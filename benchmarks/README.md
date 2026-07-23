# fmcad26 experiments — run book

`update_comparison.py` runs every experiment of the paper's comparison
table and maintains `~/paper-fmcad26-liastar/scripts/comparison.csv`.

## One command runs everything

```bash
python3 benchmarks/update_comparison.py
```

That executes all 18 runs (3 sections × 6 configurations), saving
`comparison.csv` after each one, so an interrupted run keeps its completed
results. If `comparison.csv` does not exist, it is constructed from
scratch (header + one row per benchmark); delete it to force a clean
rebuild. A full fresh run takes on the order of 1–2 hours, dominated by
per-benchmark timeouts.

Scoping options:

```bash
python3 benchmarks/update_comparison.py --only sets          # one section: sets | bags | sql
python3 benchmarks/update_comparison.py --configs cvc5       # some configurations
python3 benchmarks/update_comparison.py 60 -j 8              # timeout 60s, 8 parallel jobs
python3 benchmarks/update_comparison.py --parse-only         # no runs; re-read result csvs
```

## Benchmarks

The canonical set lives in `fmcad26/`, one `comparison.csv` row per file:

| section | files | count |
|---|---|---|
| sets (`bapa`) | `fmcad26/arith/cvc5_bapa/`, `fmcad26/card/cvc5_bapa/` | 240 |
| bags (`mapa`) | `fmcad26/arith/cvc5_mapa/`, `fmcad26/card/cvc5_mapa/` | 240 |
| sql | `fmcad26/sql/linear/` | 29 |

These are cvc5-format smt2 files (`int.star-contains`). The sets/bags
ones were generated from the **native** benchmarks in
`benchmarks/bapa/{arith,card}/fol_*.smt2` (z3 format, read by
`lia_star_solver.py`); `fol_N` corresponds to `fol_N` across encodings,
which is how rows line up positionally in `comparison.csv`.

## The six configurations

Each owns one file/result/duration column triple of `comparison.csv`, in
this column order:

| configuration | tool and input |
|---|---|
| `unfold0`, `unfold5`, `no_interp` | **SLS solver.** Sets/bags: `lia_star_solver.py` on the *native* benchmarks (`--mapa` for bags). Sql: `smt_to_sls.py` (translator) on the fmcad26 files, since sql has no native form. |
| `cvc5` | the liastar cvc5 binary (`~/cvc5/liastar/build/bin/cvc5 <file> --tlimit=<ms>`) on the fmcad26 files |
| `sqlsolver` | SQLSolver pipeline, **original** (modification commit reverted — see below) |
| `modified_sqlsolver` | SQLSolver pipeline, **modified** (HEAD of `~/SQLSolver`) |

Why SLS runs the native files: routing sets/bags through the
`smt_to_sls.py` translator was measured to hurt SLS badly (bapa unfold0:
53 timeouts via the translator vs 20 natively, July 2026). The file
column of each configuration records what it actually ran.

The SLS runs need the repo's `.venv` (has the `cvc5` and `z3` python
packages — see `install.sh`); the script picks `.venv/bin/python3`
automatically when present.

## The SQLSolver flavors

Both flavors run the same JUnit tests of
`~/SQLSolver/superopt/src/test/java/sqlsolver/superopt/liastar/SmtBenchmarks.java`
(`runAllBapaBenchmarks`, `runAllMapaBenchmarks`,
`runLinearSqlSolverBenchmarks` — all pointed at the fmcad26 directories):

- `modified_sqlsolver` runs `~/SQLSolver` HEAD as-is.
- `sqlsolver` reverse-applies the diff of the modification commit
  `e2acacee3506fef2372313db2fddf6f6659e57ea` ("overapproximation
  unknown") to the working tree, runs, and restores `superopt/src/main`
  from HEAD afterwards.

Both abort unless `superopt/src/main` is free of uncommitted changes, and
gradle recompiles the pipeline on every flip (`--rerun-tasks` forces
fresh test execution). **Do not edit `~/SQLSolver` while a run is in
progress.** If the modification is ever rebased/squashed, update
`MODIFICATION_COMMIT` in `update_comparison.py`.

The tests write `sql_bapa.csv` / `sql_mapa.csv` / `sql_solver.csv` into
the SQLSolver root; their per-benchmark 100s timeout and parallelism are
hardcoded in Java (`runMultipleBenchmarks`), so the script's TIMEOUT
argument does not apply to these two configurations. The sql test runs
sequentially on purpose (fast benchmarks, accurate timings); the others
use all CPUs but two.

## Outputs

- `benchmarks/output/<section>_<config>.csv` — one result file per run,
  `filename,result,duration` rows in benchmark order (Excel-friendly).
  These are what `--parse-only` re-reads. (`*_stats.csv` files in the
  same directory are historical solver statistics from earlier
  `run_bapa.py`-era runs; the current script does not produce them.)
- `comparison.csv` — 18 columns (6 × file/result/duration), 509 data
  rows (240 sets, 240 bags, 29 sql, in that order), CRLF line endings,
  results lowercase throughout: `sat`, `unsat`, `unknown`, `timeout`,
  `error`.

## Parallelism and timing fidelity

Sets/bags benchmarks run in parallel (default: all CPUs but two; `-j`
overrides), the sql section sequentially. Parallel runs inflate measured
durations somewhat through CPU contention — use a small `-j` when timing
fidelity matters more than wall-clock. The worker pool uses threads
deliberately: each job only waits on a solver subprocess (the GIL is
released), so processes would add overhead without adding parallelism.

## Sanity checking a fresh run

A quick cross-tool contradiction check over the final csv (a row where
one tool says `sat` and another `unsat` indicates a soundness bug
somewhere):

```bash
awk -F, 'NR>1 {s=0; u=0; for (i=2; i<=17; i+=3) {if ($i=="sat") s=1; if ($i=="unsat") u=1}
               if (s&&u) print "CONTRADICTION: " $1}' \
    ~/paper-fmcad26-liastar/scripts/comparison.csv
```

Known instance (July 2026): `card/cvc5_bapa/fol_0000116.smt2` — original
sqlsolver answers `sat`, cvc5 (and the test suite's expectation) says
`unsat`; the modified pipeline returns `unknown` there, which is the
point of the modification.
