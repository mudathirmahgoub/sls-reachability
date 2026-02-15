import os
import csv
import subprocess

dirs = ["benchmarks/bapa/arith/cvc5","benchmarks/bapa/card/cvc5"]
output_csv = "cvc5_arith.csv"

with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["filename", "result"])
    for dir in dirs:
        files = sorted(os.listdir(dir))
        for filename in files:
            path = os.path.join(dir, filename)

            if os.path.isfile(path):
                print(f"{path}")
                result = subprocess.run(
                    ["/home/mudathir/all/cvc5/liastar/build/bin/cvc5", path],
                    capture_output=True,
                    text=True
                )

                content = result.stdout.strip()
                writer.writerow([path, content])