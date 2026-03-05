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
                        ["/home/mudathir/all/cvc5/liastar/build/bin/cvc5", path, "--tlimit=50000"],
                        capture_output=True,
                        text=True,
                    )
                    end = time.time()
                    content = result.stdout.strip()
                    duration = end - start
                    print(duration)
                    writer.writerow([path, content, duration])

# dirs = ["benchmarks/bapa/arith/cvc5_bapa", "benchmarks/bapa/card/cvc5_bapa"]
# output_csv = "cvc5_arith_papa.csv"
# run_cvc5(dirs, output_csv)

dirs = ["benchmarks/bapa/arith/cvc5_mapa", "benchmarks/bapa/card/cvc5_mapa"]
output_csv = "cvc5_arith_mapa.csv"
run_cvc5(dirs, output_csv)