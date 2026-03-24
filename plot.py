import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Load CSV ===
df = pd.read_csv("comparison_mapa.csv")

# === Filter out timeouts ===
df_sls = df[df["sls result"].str.strip() != "timeout"]
df_cvc5_lia = df[df["cvc5 lia result"].str.strip() != "timeout"]
df_normaliz = df[df["lia normaliz result"].str.strip() != "timeout"]

# === Extract and sort durations ===
column_cvc5_lia = df_cvc5_lia["cvc5 lia duration"].astype(float).sort_values().tolist()
column_sls  = df_sls["sls duration"].astype(float).sort_values().tolist()
column_normaliz  = df_normaliz["lia normaliz duration"].astype(float).sort_values().tolist()

# === Compute cumulative sums ===
cvc5_cum = np.cumsum(column_cvc5_lia)
sls_cum  = np.cumsum(column_sls)
normaliz_cum  = np.cumsum(column_normaliz)

cvc5_lia= list(range(1, len(cvc5_cum) + 1))
sls  = list(range(1, len(sls_cum) + 1))
normaliz  = list(range(1, len(normaliz_cum) + 1))

# === Plot ===
plt.figure(figsize=(10, 6))
plt.plot(cvc5_cum, cvc5_lia, label="cvc5 lia", linewidth=2)
plt.plot(sls_cum, sls, label="sls",  linewidth=2)
plt.plot(normaliz_cum, normaliz, label="cvc5 lia normaliz",  linewidth=2)

plt.xlabel("Cumulative time (s)")
plt.ylabel("Number of solved instances")
plt.title("Cactus Plot: Solver Performance")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()

plt.show()