#!/usr/bin/env python3

"""
Run the paper's benchmarks and update the comparison.csv of the paper.

Three benchmark groups are supported, each in the three configurations
unfold0 / unfold5 / no_interp:

    sets (BAPA):  bapa_unfold0    bapa_unfold5    bapa_no_interp
    bags (MAPA):  mapa_unfold0    mapa_unfold5    mapa_no_interp   (--mapa)
    sql:          sql_unfold0     sql_unfold5     sql_no_interp    sql_cvc5

Sets and bags run the 240 bapa benchmarks through lia_star_solver.py, e.g.

    python3 lia_star_solver.py benchmarks/bapa/arith/fol_0000001.smt2 \\
            -i --unfold=5 --mapa

The sql group runs the benchmarks in benchmarks/sql/linear/ (copied from
SQLSolver/cvc5/linear) through smt_to_sls.py using the cvc5-enabled .venv
interpreter, e.g.

    .venv/bin/python3 smt_to_sls.py benchmarks/sql/linear/calcite-query013-call-0.smt2 \\
            --unfold=5

and additionally through the liastar cvc5 binary itself (the sql_cvc5
configuration, filling the "cvc5 lia" columns of comparison.csv):

    ~/cvc5/liastar/build/bin/cvc5 benchmarks/sql/linear/... --tlimit=100000

Pipeline
--------
1. run: every configuration runs all its benchmarks and writes <name>.txt
   (and, for sets/bags, <name>.csv with solver statistics) into the output
   directory (default: benchmarks/output/).
2. parse: the txt files are parsed as colon-separated values, stripping all
   padding spaces.
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

# The sql group additionally runs the liastar cvc5 binary on the same smt2
# files; it owns the "cvc5 lia" columns of comparison.csv
CVC5_BINARY = os.path.expanduser("~/cvc5/liastar/build/bin/cvc5")
SQL_CONFIGS = CONFIGS + [Config("cvc5", [], column=3)]

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

SQL_BENCHMARKS = sorted(
    "sql/linear/" + f
    for f in os.listdir(os.path.join(SCRIPT_DIR, "sql", "linear"))
    if f.endswith(".smt2"))

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
    cmd = [CVC5_BINARY, os.path.join(SCRIPT_DIR, benchmark),
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
    """Write <name>.txt (and <name>.csv when solver statistics are
    available) into out_dir, in benchmark order (results may arrive in
    completion order)."""
    os.makedirs(out_dir, exist_ok=True)
    txt_path = os.path.join(out_dir, name + ".txt")

    with open(txt_path, "w") as txt:
        for benchmark in benchmarks:
            result, duration, _ = results[benchmark]
            txt.write("{} : {} : {}\n".format(
                benchmark.ljust(27), result.rjust(7), duration))
    written = txt_path

    # a stats csv (run_bapa.py's format) only makes sense if the solver
    # reported statistics beyond the benchmark name
    if any(len(stats) > 1 for _, _, stats in results.values()):
        csv_path = os.path.join(out_dir, name + ".csv")
        with open(csv_path, "w", newline="") as csvf:
            writer = csv.DictWriter(csvf, fieldnames=STATS_FIELDS)
            writer.writeheader()
            for benchmark in benchmarks:
                writer.writerow(results[benchmark][2])
        written += " and " + csv_path

    print("  wrote {}".format(written), flush=True)


# ---------------------------------------------------------------------------
# Updating comparison.csv
# ---------------------------------------------------------------------------

def parse_txt(path):
    """Parse a generated txt file into {benchmark: (result, duration)},
    treating ':' as the delimiter and stripping all padding spaces."""
    results = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                head, duration = line.rsplit(":", 1)
                benchmark, result = head.split(":", 1)
                float(duration)
            except ValueError:
                print("  WARNING: skipping unparseable line: {!r}".format(
                    line))
                continue
            results[benchmark.strip()] = (result.strip(), duration.strip())
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
        print("  {}: WARNING: no txt entry for {} benchmarks (e.g. {})"
              .format(label, len(missing), missing[0]))


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
                        "txt files and update the csv")
    p.add_argument("--only", choices=["sets", "bags", "sql"],
                   help="run/update only the sets (bapa), bags (mapa) or "
                        "sql group")
    p.add_argument("--configs", metavar="NAME[,NAME...]", default=None,
                   help="run/update only these configurations "
                        "(unfold0, unfold5, no_interp, cvc5; default: all)")
    args = p.parse_args()
    args.configs = args.configs.split(",") if args.configs else None
    return args


def update_from_txt(rows, csv_path, out_dir, name, section_rows, column):
    """Parse out_dir/<name>.txt into the given comparison.csv rows and save
    the file, so every finished configuration is persisted immediately."""
    txt = os.path.join(out_dir, name + ".txt")
    if not os.path.exists(txt):
        print("  {}: WARNING: {} not found, skipping".format(name, txt))
        return
    update_rows(section_rows, parse_txt(txt), column, name)
    write_comparison(csv_path, rows)


def main():
    args = parse_args()
    rows = read_comparison(args.csv)

    # sets and bags: fixed-position sections of comparison.csv
    for section in SECTIONS:
        if args.only in ("sql", "sets" if section.mapa else "bags"):
            continue
        for config in CONFIGS:
            if args.configs and config.name not in args.configs:
                continue
            name = "{}_{}".format(section.prefix, config.name)
            if not args.parse_only:
                run_configuration(name, BAPA_BENCHMARKS, solve_bapa,
                                  args.timeout, section.mapa,
                                  config.solver_args,
                                  args.jobs or DEFAULT_JOBS, args.out_dir)
            section_rows = rows[1 + section.row:
                                1 + section.row + SECTION_SIZE]
            update_from_txt(rows, args.csv, args.out_dir, name,
                            section_rows, config.column)

    # sql: rows appended after the bapa/mapa sections as needed
    if args.only in (None, "sql"):
        ensure_sql_rows(rows)
        sql_rows = rows[1 + len(SECTIONS) * SECTION_SIZE:]
        for config in SQL_CONFIGS:
            if args.configs and config.name not in args.configs:
                continue
            solver = solve_cvc5 if config.name == "cvc5" else solve_sql
            name = "sql_{}".format(config.name)
            if not args.parse_only:
                run_configuration(name, SQL_BENCHMARKS, solver,
                                  args.timeout, False, config.solver_args,
                                  args.jobs or 1, args.out_dir)
            update_from_txt(rows, args.csv, args.out_dir, name,
                            sql_rows, config.column)

    print("\nUpdated {}".format(args.csv))


if __name__ == "__main__":
    main()
