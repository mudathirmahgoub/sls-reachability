import csv
import subprocess
import sys
import time
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SMT_TO_SLS = SCRIPT_DIR / "smt_to_sls.py"
INPUT_CSV = SCRIPT_DIR / "sql_files.csv"
OUTPUT_CSV = SCRIPT_DIR / "results.csv"
TIMEOUT_SECONDS = 100

VENV_PYTHON = SCRIPT_DIR / ".venv" / "bin" / "python3"
PYTHON_EXE = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable


def run_one(filename: str) -> tuple[str, float]:
    start = time.time()
    try:
        command = [PYTHON_EXE, str(SMT_TO_SLS), filename]
        print(command)
        proc = subprocess.run(command,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return "timeout", time.time() - start

    duration = time.time() - start
    if proc.returncode != 0:
        return "error", duration

    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    result = lines[-2].strip() if lines else "unknown"
    return result, duration


def main():
    with open(INPUT_CSV) as f:
        filenames = [line.strip() for line in f if line.strip()]

    with open(OUTPUT_CSV, "w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["filename", "result", "duration"])
        for i, filename in enumerate(filenames, 1):
            print(f"[{i}/{len(filenames)}] {filename}", flush=True)
            result, duration = run_one(filename)
            print(f"    -> {result} in {duration:.2f}s", flush=True)
            writer.writerow([filename, result, f"{duration:.3f}"])
            out.flush()


if __name__ == "__main__":
    main()
