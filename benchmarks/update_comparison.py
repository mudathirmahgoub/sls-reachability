#!/usr/bin/env python3

"""
Run all bapa benchmarks in parallel and update the paper's comparison.csv.

The six configurations of the comparison table are executed one after the
other; within a configuration, the 240 benchmarks run in parallel:

    sets (BAPA):  bapa_unfold0    bapa_unfold5    bapa_no_interp
    bags (MAPA):  mapa_unfold0    mapa_unfold5    mapa_no_interp   (--mapa)

Each benchmark is a single solver invocation, e.g.

    python3 lia_star_solver.py benchmarks/bapa/arith/fol_0000001.smt2 \\
            -i --unfold=5 --mapa

with the same per-benchmark timeout and error handling as run_bapa.py.

Pipeline
--------
1. run: every configuration runs all benchmarks in a worker pool and writes
   <name>.txt and <name>.csv (run_bapa.py's formats) into the output
   directory (default: benchmarks/output/, which is git-ignored).
2. parse: the txt files are parsed as colon-separated values, stripping all
   padding spaces.
3. update: the results are written into the unfold0 / unfold5 / no_interp
   columns of comparison.csv. Data rows 1-240 of that csv hold the sets
   results, rows 241-480 the bags results; the cvc5 and sqlsolver columns
   are never touched. comparison.csv is saved after every configuration, so
   an interrupted run keeps its completed results.

Concurrency
-----------
The pool is a ThreadPoolExecutor, not a ProcessPoolExecutor, and that is
deliberate: each job only calls subprocess.run(), i.e. it spawns a solver
process and blocks until it exits. All CPU work happens in those solver
processes, and a thread blocked in subprocess.run() releases the GIL, so
threads already provide full parallelism. Worker processes would only add
interpreter-spawn and pickling overhead (measured: 12 benchmarks / 6
workers -> threads 0.70s, processes 0.80s, sequential 2.34s).

By default two CPUs are left free for the operating system and the IDE.
Note that heavy parallelism can still inflate the measured solver times
through CPU contention; use -j to trade wall-clock time for fidelity.

Usage
-----
    python3 update_comparison.py 100            # full run, timeout 100s
    python3 update_comparison.py 100 -j 8       # at most 8 solvers at once
    python3 update_comparison.py --only bags    # mapa configurations only
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
SOLVER = os.path.join(REPO_DIR, "lia_star_solver.py")

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

# A section is one half of comparison.csv: `row` is its first data row
# (0-based, header excluded). Sets rows come first, bags rows second.
Section = namedtuple("Section", ["prefix", "mapa", "row"])
SECTIONS = [
    Section("bapa", mapa=False, row=0),    # sets: data rows 0-239
    Section("mapa", mapa=True,  row=240),  # bags: data rows 240-479
]

# Benchmark names as they appear in the txt files and in comparison.csv,
# relative to the benchmarks directory
BENCHMARKS = ["{}/fol_{:07d}.smt2".format(d, i)
              for d in ("bapa/arith", "bapa/card")
              for i in range(1, 121)]
SECTION_SIZE = len(BENCHMARKS)  # 120 arith + 120 card = 240

# Columns of the per-configuration statistics csv, as written by run_bapa.py
STATS_FIELDS = [
    "name", "sat", "problem_size", "sls_size", "z3_calls",
    "interpolants_generated", "merges", "shiftdowns", "offsets",
    "total_time", "reduction_time", "augment_time", "interpolation_time",
    "solution_time",
]


# ---------------------------------------------------------------------------
# Running the solver
# ---------------------------------------------------------------------------

def solve(benchmark, timeout, mapa, solver_args):
    """Run lia_star_solver.py on a single benchmark.

    Timeout and error handling mirror run_bapa.py. Returns
    (benchmark, result, duration, stats) where result is 'sat', 'unsat',
    'timeout' or 'ERROR ...'.
    """
    cmd = [sys.executable, SOLVER, os.path.join(SCRIPT_DIR, benchmark), "-i"]
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


def run_configuration(name, timeout, mapa, solver_args, jobs, out_dir):
    """Run all benchmarks of one configuration in a worker pool, then write
    <name>.txt and <name>.csv (run_bapa.py's formats) into out_dir."""
    print("\n=== {}: {} benchmarks, {} parallel jobs, timeout {}s ===".format(
        name, len(BENCHMARKS), jobs, timeout), flush=True)

    # Threads, not processes: each job just waits on a solver subprocess,
    # which releases the GIL (see the module docstring)
    results = {}
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = [pool.submit(solve, b, timeout, mapa, solver_args)
                   for b in BENCHMARKS]
        for done, future in enumerate(as_completed(futures), 1):
            benchmark, result, duration, stats = future.result()
            results[benchmark] = (result, duration, stats)
            print("  [{}/{}] {} : {} : {:.2f}s".format(
                done, len(BENCHMARKS), benchmark, result, duration),
                flush=True)

    write_run_files(name, results, out_dir)


def write_run_files(name, results, out_dir):
    """Write <name>.txt and <name>.csv into out_dir, in benchmark order
    (results arrive in completion order)."""
    os.makedirs(out_dir, exist_ok=True)
    txt_path = os.path.join(out_dir, name + ".txt")
    csv_path = os.path.join(out_dir, name + ".csv")

    with open(txt_path, "w") as txt, open(csv_path, "w", newline="") as csvf:
        writer = csv.DictWriter(csvf, fieldnames=STATS_FIELDS)
        writer.writeheader()
        for benchmark in BENCHMARKS:
            result, duration, stats = results[benchmark]
            txt.write("{} : {} : {}\n".format(
                benchmark.ljust(27), result.rjust(7), duration))
            writer.writerow(stats)

    print("  wrote {} and {}".format(txt_path, csv_path), flush=True)


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


def update_rows(rows, results, section_row, column, label):
    """Write result/duration into one configuration's columns of one
    section, matching rows by the benchmark name in the config's file
    column (stripped: some legacy cells carry padding spaces)."""
    updated, missing = 0, []
    for row in rows[1 + section_row: 1 + section_row + SECTION_SIZE]:
        benchmark = row[column].strip()
        if benchmark in results:
            row[column] = benchmark
            row[column + 1], row[column + 2] = results[benchmark]
            updated += 1
        else:
            missing.append(benchmark)

    print("  {}: updated {}/{} rows".format(label, updated, SECTION_SIZE))
    if missing:
        print("  {}: WARNING: no txt entry for {} benchmarks (e.g. {})"
              .format(label, len(missing), missing[0]))


def read_comparison(path):
    """Read comparison.csv and check it has the expected shape."""
    with open(path, newline="") as f:
        rows = list(csv.reader(f))
    expected = 1 + len(SECTIONS) * SECTION_SIZE
    if len(rows) != expected:
        sys.exit("error: {} has {} rows, expected {}".format(
            path, len(rows), expected))
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
    p.add_argument("-j", "--jobs", type=int, default=DEFAULT_JOBS,
                   help="number of benchmarks to run in parallel (default: "
                        "all cpus but two, here {})".format(DEFAULT_JOBS))
    p.add_argument("--csv", default=DEFAULT_CSV,
                   help="comparison.csv to update (default: {})".format(
                       DEFAULT_CSV))
    p.add_argument("--out-dir", default=DEFAULT_OUT_DIR,
                   help="directory for all generated txt/csv files "
                        "(default: benchmarks/output, git-ignored)")
    p.add_argument("--parse-only", action="store_true",
                   help="do not run the benchmarks; just parse existing "
                        "txt files and update the csv")
    p.add_argument("--only", choices=["sets", "bags"],
                   help="run/update only the sets (bapa) or bags (mapa) half")
    return p.parse_args()


def main():
    args = parse_args()
    rows = read_comparison(args.csv)

    for section in SECTIONS:
        if args.only == "sets" and section.mapa:
            continue
        if args.only == "bags" and not section.mapa:
            continue

        for config in CONFIGS:
            name = "{}_{}".format(section.prefix, config.name)
            if not args.parse_only:
                run_configuration(name, args.timeout, section.mapa,
                                  config.solver_args, args.jobs, args.out_dir)

            txt = os.path.join(args.out_dir, name + ".txt")
            if not os.path.exists(txt):
                print("  {}: WARNING: {} not found, skipping".format(
                    name, txt))
                continue
            update_rows(rows, parse_txt(txt), section.row, config.column,
                        name)
            # save progress after every configuration
            write_comparison(args.csv, rows)

    print("\nUpdated {}".format(args.csv))


if __name__ == "__main__":
    main()
