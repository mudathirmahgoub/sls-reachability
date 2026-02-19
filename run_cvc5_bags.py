import os
import csv
import subprocess
import time


def run_cvc5(dirs, output_csv):
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
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
                        ["/home/mudathir/all/cvc5/liastar/build/bin/cvc5", path, "--parse-only"],
                        capture_output=True,
                        text=True,
                    )
                    end = time.time()
                    content = result.stdout.strip()
                    duration = end - start
                    print(duration)
                    print(content)
                    writer.writerow([path, content, duration])

dirs = ["benchmarks/bags/arith", "benchmarks/bags/card"]
output_csv = "cvc5_bags.csv"
run_cvc5(dirs, output_csv)
