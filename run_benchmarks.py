import os
import csv
import subprocess

directory = "benchmarks/bapa/arith"
output_csv = "cvc5_arith.csv"

with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["filename", "result"])

    files = sorted(os.listdir(directory))
    for filename in files:
        path = os.path.join(directory, filename)

        if os.path.isfile(path):
            print(f"{path}")
            result = subprocess.run(
                ["/home/mudathir/all/sls-reachability/.venv/bin/python3", "lia_star_solver.py", path,  "--mapa", "--unfold=5"],
                capture_output=True,
                text=True,
                timeout=50
            )

            content = result.stdout.strip()
            writer.writerow([filename, content])