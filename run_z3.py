import os
import csv
import subprocess
import time


def run_cvc5(dirs, output_csv):
    with open(output_csv, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename", "result", "duration"])
        for dir in dirs:
            files = sorted(os.listdir(dir))
            for filename in files:
                path = os.path.join(dir, filename)
                if os.path.isfile(path):
                    print(f"{path}")
                    start = time.time()
                    result = subprocess.run(
                        ["/home/mudathir/all/sls-reachability/.venv/bin/z3","timeout=50000", path],
                        capture_output=True,
                        text=True,
                    )
                    end = time.time()
                    content = result.stdout.strip()
                    duration = end - start
                    print(duration)
                    split = content.split("\n")
                    print(split)
                    print(len(split))
                    if len(split) >= 2:
                        content = split[1]
                    else:
                        content = "error"
                    writer.writerow([path, content, duration])

dirs = ["benchmarks/bapa/arith", "benchmarks/bapa/card"]
output_csv = "z3_sets.csv"
run_cvc5(dirs, output_csv)
