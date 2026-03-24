import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Load CSV ===
df = pd.read_csv("comparison_mapa.csv")

# === Filter out timeouts ===
df_sls = df[df["sls result"].str.strip() != "timeout"]
df_cvc5 = df[df["cvc5 lia result"].str.strip() != "timeout"]

# === Extract and sort durations ===
cvc5 = df_cvc5["cvc5 lia duration"].astype(float).sort_values().tolist()
sls  = df_sls["sls duration"].astype(float).sort_values().tolist()

# === Compute cumulative sums ===
cvc5_cum = np.cumsum(cvc5)
sls_cum  = np.cumsum(sls)

# === X-axis: number of solved instances ===
z_cvc5 = list(range(1, len(cvc5_cum) + 1))
z_sls  = list(range(1, len(sls_cum) + 1))

# === Plot ===
plt.figure(figsize=(10, 6))
plt.plot(cvc5_cum, z_cvc5, label="cvc5 lia", linewidth=2)
plt.plot(sls_cum, z_sls, label="sls",  linewidth=2)

plt.xlabel("Cumulative time (s)")
plt.ylabel("Number of solved instances")
plt.title("Cactus Plot: Solver Performance")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

plt.show()