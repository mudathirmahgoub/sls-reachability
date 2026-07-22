#!/usr/bin/env python3

"""
Run the paper's benchmarks and update the comparison.csv of the paper.

Three benchmark groups are supported, each in the three configurations
unfold0 / unfold5 / no_interp:

    sets (BAPA):  bapa_unfold0  bapa_unfold5  bapa_no_interp  bapa_cvc5
                  bapa_sqlsolver  bapa_modified_sqlsolver
    bags (MAPA):  mapa_unfold0  mapa_unfold5  mapa_no_interp  mapa_cvc5
                  mapa_sqlsolver  mapa_modified_sqlsolver     (--mapa)
    sql:          sql_unfold0   sql_unfold5   sql_no_interp   sql_cvc5
                  sql_sqlsolver   sql_modified_sqlsolver

Sets and bags run the 240 bapa benchmarks through lia_star_solver.py, e.g.

    python3 lia_star_solver.py benchmarks/bapa/arith/fol_0000001.smt2 \\
            -i --unfold=5 --mapa

Their cvc5 configurations run the liastar cvc5 binary on the translated
benchmarks in benchmarks/bapa/*/cvc5_bapa/ (sets) and cvc5_mapa/ (bags),
which are the files the "cvc5" columns of comparison.csv refer to.

The sql group runs the benchmarks in benchmarks/sql/linear/ (copied from
SQLSolver/cvc5/linear) through smt_to_sls.py using the cvc5-enabled .venv
interpreter, e.g.

    .venv/bin/python3 smt_to_sls.py benchmarks/sql/linear/calcite-query013-call-0.smt2 \\
            --unfold=5

and additionally through the liastar cvc5 binary itself (the sql_cvc5
configuration, filling the "cvc5 lia" columns of comparison.csv):

    ~/cvc5/liastar/build/bin/cvc5 benchmarks/sql/linear/... --tlimit=100000

and through the SQLSolver pipeline: the *_sqlsolver configurations fill
the "sqlsolver" columns, the *_modified_sqlsolver configurations the
"modified_sqlsolver" ones. Each of those is a single gradle invocation of
a JUnit test of SmtBenchmarks in ~/SQLSolver (runLinearSqlSolverBenchmarks
/ runAllBapaBenchmarks / runAllMapaBenchmarks) running SQLSolver's own
copy of the same smt2 files and writing a filename,result,duration csv.
The tests parallelize internally (except the fast sql one, which stays
sequential for accurate timings); their per-benchmark 100s timeout is
hardcoded in Java, so this script's TIMEOUT argument does not apply.

Both sqlsolver flavors run the SAME tests -- which pipeline they measure
depends on the state of the ~/SQLSolver working tree. The convention this
script enforces before running (and cannot check with --parse-only):

    sqlsolver           requires superopt/src/main to have NO uncommitted
                        changes (the original, committed pipeline)
    modified_sqlsolver  requires uncommitted changes under
                        superopt/src/main (your modifications)

so switch the tree (git stash / git stash pop) to flip between them.
Gradle recompiles the pipeline automatically on every run.

Pipeline
--------
1. run: every configuration runs all its benchmarks and writes <name>.csv
   with filename,result,duration rows -- a format Excel opens directly --
   (and, where the solver reports statistics, <name>_stats.csv) into the
   output directory (default: benchmarks/output/).
2. parse: the result csv files are read back, stripping any padding spaces.
3. update: the results are written into the unfold0 / unfold5 / no_interp
   columns of comparison.csv. Data rows 1-240 hold the sets results, rows
   241-480 the bags results, and the sql results follow after them (rows
   for missing sql benchmarks are appended with all other columns left
   empty, to be filled by later runs). The cvc5 and sqlsolver columns are
   never touched. comparison.csv is saved after every configuration, so an
   interrupted run keeps its completed results.

Concurrency
-----------
Sets and bags use a ThreadPoolExecutor, not a ProcessPoolExecutor, and that
is deliberate: each job only calls subprocess.run(), i.e. it spawns a
solver process and blocks until it exits. All CPU work happens in those
solver processes, and a thread blocked in subprocess.run() releases the
GIL, so threads already provide full parallelism. Worker processes would
only add interpreter-spawn and pickling overhead (measured: 12 benchmarks /
6 workers -> threads 0.70s, processes 0.80s, sequential 2.34s).

By default two CPUs are left free for the operating system and the IDE.
Note that heavy parallelism can still inflate the measured solver times
through CPU contention; use -j to trade wall-clock time for fidelity. The
sql benchmarks are fast (mostly well under a second), so they run
sequentially by default for accurate timings; -j overrides that too.

Usage
-----
    python3 update_comparison.py 100            # everything, timeout 100s
    python3 update_comparison.py --only sql     # sql group only, sequential
    python3 update_comparison.py --only sql --configs cvc5   # one config only
    python3 update_comparison.py 100 -j 8       # at most 8 solvers at once
    python3 update_comparison.py --parse-only   # skip runs, just update csv
"""

import argparse
import ast
import csv
import os
import subprocess
import sys
import time
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor, as_completed


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))   # .../benchmarks
REPO_DIR = os.path.dirname(SCRIPT_DIR)                    # repository root
BAPA_SOLVER = os.path.join(REPO_DIR, "lia_star_solver.py")
SQL_SOLVER = os.path.join(REPO_DIR, "smt_to_sls.py")

# smt_to_sls.py needs the cvc5 package, which lives in the repo's .venv
VENV_PYTHON = os.path.join(REPO_DIR, ".venv", "bin", "python3")
SQL_PYTHON = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

DEFAULT_OUT_DIR = os.path.join(SCRIPT_DIR, "output")
DEFAULT_CSV = os.path.expanduser(
    "~/paper-fmcad26-liastar/scripts/comparison.csv")

# Leave two CPUs free for the operating system and the IDE
DEFAULT_JOBS = max(1, (os.cpu_count() or 3) - 2)

# A configuration owns three adjacent columns of comparison.csv, starting at
# `column`: "<name> file", "<name> result", "<name> duration".
Config = namedtuple("Config", ["name", "solver_args", "column"])
CONFIGS = [
    Config("unfold0",   ["--unfold=0"],  column=0),
    Config("unfold5",   ["--unfold=5"],  column=6),
    Config("no_interp", ["--no-interp"], column=9),
]

# The cvc5 configuration runs the liastar cvc5 binary: in the sql group on
# the same smt2 files, in the sets/bags groups on the translated benchmarks
# under cvc5_bapa/ and cvc5_mapa/. It owns the "cvc5" columns of
# comparison.csv. The sql group's modified_sqlsolver configuration runs the
# modified SQLSolver pipeline and owns the "modified_sqlsolver" columns.
CVC5_BINARY = os.path.expanduser("~/cvc5/liastar/build/bin/cvc5")
CVC5_CONFIG = Config("cvc5", [], column=3)
SQLSOLVER_CONFIG = Config("sqlsolver", [], column=12)
MODIFIED_CONFIG = Config("modified_sqlsolver", [], column=15)
SQLSOLVER_FLAVORS = ("sqlsolver", "modified_sqlsolver")
BAPA_CONFIGS = CONFIGS + [CVC5_CONFIG, SQLSOLVER_CONFIG, MODIFIED_CONFIG]
SQL_CONFIGS = CONFIGS + [CVC5_CONFIG, SQLSOLVER_CONFIG, MODIFIED_CONFIG]

# Per group: the SmtBenchmarks JUnit test that runs the modified SQLSolver
# pipeline on it, and the csv file the test writes into the SQLSolver root
SQLSOLVER_DIR = os.path.expanduser("~/SQLSolver")
SQLSOLVER_TESTS = {
    "sql":  ("runLinearSqlSolverBenchmarks", "sql_solver.csv"),
    "bapa": ("runAllBapaBenchmarks",         "sql_bapa.csv"),
    "mapa": ("runAllMapaBenchmarks",         "sql_mapa.csv"),
}

# A section is one fixed-position block of comparison.csv: `row` is its
# first data row (0-based, header excluded). Sets rows come first, bags
# rows second; the sql rows follow after both sections.
Section = namedtuple("Section", ["prefix", "mapa", "row"])
SECTIONS = [
    Section("bapa", mapa=False, row=0),    # sets: data rows 0-239
    Section("mapa", mapa=True,  row=240),  # bags: data rows 240-479
]

# Benchmark names as they appear in the txt files and in comparison.csv,
# relative to the benchmarks directory
BAPA_BENCHMARKS = ["{}/fol_{:07d}.smt2".format(d, i)
                   for d in ("bapa/arith", "bapa/card")
                   for i in range(1, 121)]
SECTION_SIZE = len(BAPA_BENCHMARKS)  # 120 arith + 120 card = 240

# The translated benchmarks the cvc5 binary runs on for sets/bags, named
# exactly as the "cvc5 filename" cells of comparison.csv (repo-relative)
CVC5_BENCHMARKS = {
    prefix: ["benchmarks/bapa/{}/cvc5_{}/fol_{:07d}.smt2".format(d, prefix, i)
             for d in ("arith", "card")
             for i in range(1, 121)]
    for prefix in ("bapa", "mapa")
}

SQL_BENCHMARKS = sorted(
    "sql/linear/" + f
    for f in os.listdir(os.path.join(SCRIPT_DIR, "sql", "linear"))
    if f.endswith(".smt2"))

# The benchmarks the SQLSolver pipeline runs on, named as its JUnit tests
# list them (SQLSolver's own copies, relative to its root); the sql
# group's names are renamed to sql/linear/ when parsing instead
SQLSOLVER_BENCHMARKS = {
    prefix: ["cvc5/sls-reachability/{}/cvc5_{}/fol_{:07d}.smt2".format(
                 d, prefix, i)
             for d in ("arith", "card")
             for i in range(1, 121)]
    for prefix in ("bapa", "mapa")
}
SQLSOLVER_BENCHMARKS["sql"] = SQL_BENCHMARKS

# Columns of the per-configuration statistics csv, as written by run_bapa.py
STATS_FIELDS = [
    "name", "sat", "problem_size", "sls_size", "z3_calls",
    "interpolants_generated", "merges", "shiftdowns", "offsets",
    "total_time", "reduction_time", "augment_time", "interpolation_time",
    "solution_time",
]


# ---------------------------------------------------------------------------
# Running the solvers
# ---------------------------------------------------------------------------

def solve_bapa(benchmark, timeout, mapa, solver_args):
    """Run lia_star_solver.py on a single bapa benchmark.

    Timeout and error handling mirror run_bapa.py. Returns
    (benchmark, result, duration, stats) where result is 'sat', 'unsat',
    'timeout' or 'ERROR ...'.
    """
    cmd = [sys.executable, BAPA_SOLVER,
           os.path.join(SCRIPT_DIR, benchmark), "-i"]
    cmd += solver_args
    if mapa:
        cmd.append("--mapa")

    start = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout,
                              cwd=REPO_DIR)
        duration = time.time() - start
        # with -i, stdout is: problem size / stats dict / sat|unsat / ...
        lines = proc.stdout.decode("utf-8").strip().split("\n")
        stats = ast.literal_eval(lines[1])
        stats["total_time"] = duration
        result = lines[2]

    # Solver times out
    except subprocess.TimeoutExpired:
        duration = time.time() - start
        stats = {"sat": 2, "problem_size": -1}
        result = "timeout"

    # Solver crashes or prints something unexpected
    except Exception as exc:
        duration = time.time() - start
        stats = {}
        result = "ERROR {}".format(" ".join(str(exc).split()))

    stats["name"] = benchmark
    return benchmark, result, duration, stats


def solve_sql(benchmark, timeout, mapa, solver_args):
    """Run smt_to_sls.py on a single sql benchmark (mapa is ignored; it
    exists to share solve_bapa's signature).

    Result detection mirrors run_sql.py: scan stdout for a line that is
    exactly 'sat' or 'unsat'. Returns (benchmark, result, duration, stats)
    with stats always empty (smt_to_sls.py prints no statistics).
    """
    cmd = [SQL_PYTHON, SQL_SOLVER, os.path.join(SCRIPT_DIR, benchmark)]
    cmd += solver_args

    start = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout,
                              cwd=REPO_DIR)
        duration = time.time() - start
        if proc.returncode != 0:
            result = "error"
        else:
            result = "unknown"
            for line in proc.stdout.decode("utf-8").splitlines():
                if line.strip() in ("sat", "unsat"):
                    result = line.strip()
                    break

    except subprocess.TimeoutExpired:
        duration = time.time() - start
        result = "timeout"

    return benchmark, result, duration, {"name": benchmark}


def solve_cvc5(benchmark, timeout, mapa, solver_args):
    """Run the liastar cvc5 binary on a single sql benchmark (mapa and
    solver_args are ignored; they exist to share solve_bapa's signature).

    Invocation mirrors run_cvc5.py: the timeout is also passed to cvc5 as
    --tlimit (in milliseconds), which makes it exit with 'cvc5 interrupted
    by timeout.' when hit. Returns (benchmark, result, duration, stats)
    with stats always empty.
    """
    # sql benchmark names are relative to the benchmarks directory, the
    # translated bapa/mapa ones to the repository root (matching the cells
    # of comparison.csv)
    base = REPO_DIR if benchmark.startswith("benchmarks/") else SCRIPT_DIR
    cmd = [CVC5_BINARY, os.path.join(base, benchmark),
           "--tlimit={}".format(timeout * 1000)]

    start = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout,
                              cwd=REPO_DIR)
        duration = time.time() - start
        output = (proc.stdout + proc.stderr).decode("utf-8")
        if "interrupted by timeout" in output:
            result = "timeout"
        elif proc.returncode != 0:
            result = "error"
        else:
            result = "unknown"
            for line in output.splitlines():
                if line.strip() in ("sat", "unsat", "unknown"):
                    result = line.strip()
                    break

    except subprocess.TimeoutExpired:
        duration = time.time() - start
        result = "timeout"

    return benchmark, result, duration, {"name": benchmark}


def check_sqlsolver_flavor(config_name):
    """Both sqlsolver flavors run the same JUnit tests; which pipeline they
    measure depends on the ~/SQLSolver working tree. Enforce the
    convention: 'sqlsolver' must run on a clean superopt/src/main (the
    committed pipeline), 'modified_sqlsolver' on one with uncommitted
    changes. Aborts with instructions if the tree does not match."""
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", "superopt/src/main"],
        cwd=SQLSOLVER_DIR, capture_output=True).stdout.decode().strip()
    if config_name == "sqlsolver" and status:
        sys.exit("error: cannot run the '{}' configuration: {} has "
                 "uncommitted changes under superopt/src/main:\n{}\n"
                 "stash them first (git stash) or run "
                 "--configs modified_sqlsolver instead".format(
                     config_name, SQLSOLVER_DIR, status))
    if config_name == "modified_sqlsolver" and not status:
        sys.exit("error: cannot run the '{}' configuration: {} has no "
                 "uncommitted changes under superopt/src/main, so this "
                 "would measure the unmodified pipeline; restore your "
                 "modifications (git stash pop) or run "
                 "--configs sqlsolver instead".format(
                     config_name, SQLSOLVER_DIR))


def run_sqlsolver_pipeline(config_name, prefix, name, out_dir):
    """Run the SQLSolver pipeline ('sqlsolver' or 'modified_sqlsolver',
    depending on the working-tree state, which is checked first) on one
    group's benchmarks ('sql', 'bapa' or 'mapa') and write <name>.csv into
    out_dir.

    Unlike the other runners this is one gradle invocation: the group's
    SmtBenchmarks JUnit test recompiles the pipeline, runs SQLSolver's
    copy of the benchmarks with a hardcoded 100s per-benchmark timeout (in
    parallel, except the fast sql test) and writes
    filename,result,duration rows to a csv in the SQLSolver root."""
    check_sqlsolver_flavor(config_name)
    test, test_csv = SQLSOLVER_TESTS[prefix]
    cmd = ["./gradlew", ":superopt:test", "--tests",
           "sqlsolver.superopt.liastar.SmtBenchmarks." + test,
           "--console=plain"]
    print("\n=== {}: gradle test {} ===".format(name, test), flush=True)
    subprocess.run(cmd, cwd=SQLSOLVER_DIR, check=True)

    # convert the test's csv rows to this script's benchmark names; the
    # test reports SAT/UNSAT but comparison.csv uses lowercase throughout
    results = {}
    with open(os.path.join(SQLSOLVER_DIR, test_csv), newline="") as f:
        for row in csv.DictReader(f):
            benchmark = row["filename"]
            if prefix == "sql":
                benchmark = "sql/linear/" + os.path.basename(benchmark)
            results[benchmark] = (row["result"].lower(),
                                  float(row["duration"]),
                                  {"name": benchmark})

    missing = [b for b in SQLSOLVER_BENCHMARKS[prefix] if b not in results]
    if missing:
        print("  WARNING: {} has no result for {} benchmarks (e.g. {})"
              .format(test_csv, len(missing), missing[0]))
    write_run_files(name, sorted(results), results, out_dir)


def run_configuration(name, benchmarks, solver, timeout, mapa, solver_args,
                      jobs, out_dir):
    """Run all benchmarks of one configuration through `solver` (one of the
    solve_* functions), then write the result files into out_dir.

    With jobs == 1 the benchmarks run strictly sequentially, which gives
    the most accurate timings; otherwise a thread pool runs `jobs` solver
    subprocesses at a time (threads suffice: see the module docstring).
    """
    print("\n=== {}: {} benchmarks, {}, timeout {}s ===".format(
        name, len(benchmarks),
        "sequential" if jobs == 1 else "{} parallel jobs".format(jobs),
        timeout), flush=True)

    results = {}

    def record(outcome, done):
        benchmark, result, duration, stats = outcome
        results[benchmark] = (result, duration, stats)
        print("  [{}/{}] {} : {} : {:.2f}s".format(
            done, len(benchmarks), benchmark, result, duration), flush=True)

    if jobs == 1:
        for done, benchmark in enumerate(benchmarks, 1):
            record(solver(benchmark, timeout, mapa, solver_args), done)
    else:
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            futures = [pool.submit(solver, b, timeout, mapa, solver_args)
                       for b in benchmarks]
            for done, future in enumerate(as_completed(futures), 1):
                record(future.result(), done)

    write_run_files(name, benchmarks, results, out_dir)


def write_run_files(name, benchmarks, results, out_dir):
    """Write <name>.csv with filename,result,duration rows (and
    <name>_stats.csv when solver statistics are available) into out_dir,
    in benchmark order (results may arrive in completion order)."""
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, name + ".csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "result", "duration"])
        for benchmark in benchmarks:
            result, duration, _ = results[benchmark]
            writer.writerow([benchmark, result, duration])
    written = csv_path

    # a stats csv (run_bapa.py's format) only makes sense if the solver
    # reported statistics beyond the benchmark name
    if any(len(stats) > 1 for _, _, stats in results.values()):
        stats_path = os.path.join(out_dir, name + "_stats.csv")
        with open(stats_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=STATS_FIELDS)
            writer.writeheader()
            for benchmark in benchmarks:
                writer.writerow(results[benchmark][2])
        written += " and " + stats_path

    print("  wrote {}".format(written), flush=True)


# ---------------------------------------------------------------------------
# Updating comparison.csv
# ---------------------------------------------------------------------------

def parse_results(path):
    """Parse a <name>.csv results file into {benchmark: (result,
    duration)}, stripping any padding spaces."""
    results = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            try:
                float(row["duration"])
            except (KeyError, TypeError, ValueError):
                print("  WARNING: skipping unparseable row: {!r}".format(row))
                continue
            results[row["filename"].strip()] = (row["result"].strip(),
                                                row["duration"].strip())
    return results


def update_rows(section_rows, results, column, label):
    """Write result/duration into one configuration's columns of the given
    rows, matching by the benchmark name in the config's file column
    (stripped: some legacy cells carry padding spaces)."""
    updated, missing = 0, []
    for row in section_rows:
        benchmark = row[column].strip()
        if benchmark in results:
            row[column] = benchmark
            row[column + 1], row[column + 2] = results[benchmark]
            updated += 1
        else:
            missing.append(benchmark)

    print("  {}: updated {}/{} rows".format(label, updated,
                                            len(section_rows)))
    if missing:
        print("  {}: WARNING: no result for {} benchmarks (e.g. {})"
              .format(label, len(missing), missing[0]))


def set_file_column(section_rows, benchmarks, column):
    """Overwrite a fixed-position section's file column with the given
    benchmark names, in section order. Needed when the recorded filenames
    come from another machine or layout (e.g. the modified_sqlsolver cells
    written on the original authors' machine) and can no longer be matched
    by name."""
    for row, benchmark in zip(section_rows, benchmarks):
        row[column] = benchmark


def ensure_sql_rows(rows):
    """Append a row for every sql benchmark that comparison.csv does not
    have yet, and put the benchmark name into the file column of every sql
    configuration (all four run on the same smt2 file). Everything else
    stays empty for later runs (sqlsolver, ...)."""
    width = len(rows[0])
    existing = {row[CONFIGS[0].column].strip(): row
                for row in rows[1 + len(SECTIONS) * SECTION_SIZE:]}
    added = 0
    for benchmark in SQL_BENCHMARKS:
        row = existing.get(benchmark)
        if row is None:
            row = [""] * width
            rows.append(row)
            added += 1
        for config in SQL_CONFIGS:
            if not row[config.column].strip():
                row[config.column] = benchmark
    if added:
        print("  appended {} sql rows to comparison.csv".format(added))


def read_comparison(path):
    """Read comparison.csv and check it has at least the bapa/mapa rows."""
    with open(path, newline="") as f:
        rows = list(csv.reader(f))
    minimum = 1 + len(SECTIONS) * SECTION_SIZE
    if len(rows) < minimum:
        sys.exit("error: {} has {} rows, expected at least {}".format(
            path, len(rows), minimum))
    return rows


def write_comparison(path, rows):
    # comparison.csv uses CRLF line endings; preserve them
    with open(path, "w", newline="") as f:
        csv.writer(f, lineterminator="\r\n").writerows(rows)


# ---------------------------------------------------------------------------
# Command line interface
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("timeout", metavar="TIMEOUT", nargs="?", type=int,
                   default=100,
                   help="timeout per benchmark in seconds (default: 100)")
    p.add_argument("-j", "--jobs", type=int, default=None,
                   help="number of benchmarks to run in parallel (default: "
                        "all cpus but two for sets/bags, here {}; 1 -- i.e. "
                        "sequential -- for the fast sql benchmarks)".format(
                            DEFAULT_JOBS))
    p.add_argument("--csv", default=DEFAULT_CSV,
                   help="comparison.csv to update (default: {})".format(
                       DEFAULT_CSV))
    p.add_argument("--out-dir", default=DEFAULT_OUT_DIR,
                   help="directory for all generated txt/csv files "
                        "(default: benchmarks/output)")
    p.add_argument("--parse-only", action="store_true",
                   help="do not run the benchmarks; just parse existing "
                        "result csv files and update comparison.csv")
    p.add_argument("--only", choices=["sets", "bags", "sql"],
                   help="run/update only the sets (bapa), bags (mapa) or "
                        "sql group")
    p.add_argument("--configs", metavar="NAME[,NAME...]", default=None,
                   help="run/update only these configurations (unfold0, "
                        "unfold5, no_interp, cvc5, sqlsolver, "
                        "modified_sqlsolver; default: all)")
    args = p.parse_args()
    args.configs = args.configs.split(",") if args.configs else None
    return args


def update_from_results(rows, csv_path, out_dir, name, section_rows, column):
    """Parse out_dir/<name>.csv into the given comparison.csv rows and save
    the file, so every finished configuration is persisted immediately."""
    results_csv = os.path.join(out_dir, name + ".csv")
    if not os.path.exists(results_csv):
        print("  {}: WARNING: {} not found, skipping".format(
            name, results_csv))
        return
    update_rows(section_rows, parse_results(results_csv), column, name)
    write_comparison(csv_path, rows)


def main():
    args = parse_args()
    rows = read_comparison(args.csv)

    # sets and bags: fixed-position sections of comparison.csv
    for section in SECTIONS:
        if args.only in ("sql", "sets" if section.mapa else "bags"):
            continue
        for config in BAPA_CONFIGS:
            if args.configs and config.name not in args.configs:
                continue
            name = "{}_{}".format(section.prefix, config.name)
            if not args.parse_only:
                if config.name in SQLSOLVER_FLAVORS:
                    run_sqlsolver_pipeline(config.name, section.prefix,
                                           name, args.out_dir)
                elif config.name == "cvc5":
                    run_configuration(name, CVC5_BENCHMARKS[section.prefix],
                                      solve_cvc5, args.timeout,
                                      section.mapa, config.solver_args,
                                      args.jobs or DEFAULT_JOBS,
                                      args.out_dir)
                else:
                    run_configuration(name, BAPA_BENCHMARKS, solve_bapa,
                                      args.timeout, section.mapa,
                                      config.solver_args,
                                      args.jobs or DEFAULT_JOBS,
                                      args.out_dir)
            section_rows = rows[1 + section.row:
                                1 + section.row + SECTION_SIZE]
            if config.name in SQLSOLVER_FLAVORS:
                # the recorded cells hold the original authors' paths,
                # which never match the new run's names
                set_file_column(section_rows,
                                SQLSOLVER_BENCHMARKS[section.prefix],
                                config.column)
            update_from_results(rows, args.csv, args.out_dir, name,
                                section_rows, config.column)

    # sql: rows appended after the bapa/mapa sections as needed
    if args.only in (None, "sql"):
        ensure_sql_rows(rows)
        sql_rows = rows[1 + len(SECTIONS) * SECTION_SIZE:]
        for config in SQL_CONFIGS:
            if args.configs and config.name not in args.configs:
                continue
            name = "sql_{}".format(config.name)
            if not args.parse_only:
                if config.name in SQLSOLVER_FLAVORS:
                    run_sqlsolver_pipeline(config.name, "sql", name,
                                           args.out_dir)
                else:
                    solver = (solve_cvc5 if config.name == "cvc5"
                              else solve_sql)
                    run_configuration(name, SQL_BENCHMARKS, solver,
                                      args.timeout, False,
                                      config.solver_args,
                                      args.jobs or 1, args.out_dir)
            update_from_results(rows, args.csv, args.out_dir, name,
                                sql_rows, config.column)

    print("\nUpdated {}".format(args.csv))


if __name__ == "__main__":
    main()
