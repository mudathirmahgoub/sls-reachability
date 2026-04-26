import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Load CSV ===
df = pd.read_csv("comparison_bapa.csv")

# === Filter out timeouts ===
df_sql_solver = df[df["sqlsolver result"].astype(str).str.strip() != "timeout"]
df_sls = df[df["sls result"].astype(str).str.strip() != "timeout"]
df_cvc5_lia = df[df["cvc5 lia result"].astype(str).str.strip() != "timeout"]
df_normaliz = df[df["lia normaliz result"].astype(str).str.strip() != "timeout"]

# === Extract and sort durations ===
column_sql_solver = df_cvc5_lia["sqlsolver duration"].astype(float).sort_values().tolist()
column_cvc5_lia = df_cvc5_lia["cvc5 lia duration"].astype(float).sort_values().tolist()
column_sls = df_sls["sls duration"].astype(float).sort_values().tolist()
column_normaliz = df_normaliz["lia normaliz duration"].astype(float).sort_values().tolist()

# === Compute cumulative sums ===
sql_solver_cum = np.cumsum(column_sql_solver)
cvc5_cum = np.cumsum(column_cvc5_lia)
sls_cum = np.cumsum(column_sls)
normaliz_cum = np.cumsum(column_normaliz)

sql_solver_x = list(range(1, len(sql_solver_cum) + 1))
cvc5_x = list(range(1, len(cvc5_cum) + 1))
sls_x = list(range(1, len(sls_cum) + 1))
normaliz_x = list(range(1, len(normaliz_cum) + 1))

# === Plot ===
plt.figure(figsize=(10, 6))
plt.plot(sql_solver_cum, sql_solver_x, label="sqlsolver", linewidth=2)
plt.plot(cvc5_cum, cvc5_x, label="cvc5 lia", linewidth=2)
plt.plot(sls_cum, sls_x, label="sls", linewidth=2)
# plt.plot(normaliz_cum, normaliz_x, label="normaliz", linewidth=2)

plt.xlabel("Cumulative time (s)")
plt.ylabel("Number of solved instances")
plt.title("Cactus Plot: Solver Performance in sets")
plt.grid(True, linestyle="--", alpha=0.5)

# === Magnified legend ===
plt.legend(
    fontsize=16,        # bigger text
    markerscale=2.0,    # bigger line markers
    borderpad=1.2,      # more padding inside box
    labelspacing=1.0,   # more spacing between entries
    frameon=True,
)

plt.tight_layout()

# === Save to file ===
plt.savefig("cactus_plot_bapa.png", dpi=300)

plt.show()