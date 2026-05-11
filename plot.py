import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot(source_file, output1, output2):   
    # === Load CSV ===
    df = pd.read_csv(source_file)
   
    # === Filter out timeouts ===
    df_sql_solver = df[df["sqlsolver result"].astype(str).str.strip() != "timeout"]
    df_modified_sql_solver = df[(df["modified_sqlsolver result"].astype(str).str.strip() != "timeout") &
                                   (df["modified_sqlsolver result"].astype(str).str.strip() != "unknown")]
    df_sls = df[df["sls result"].astype(str).str.strip() != "timeout"]
    df_cvc5_lia = df[df["cvc5 lia result"].astype(str).str.strip() != "timeout"]
    # df_normaliz = df[df["lia normaliz result"].astype(str).str.strip() != "timeout"]
    df_unfold5 = df[df["unfold5 result"].astype(str).str.strip() != "timeout"]
    df_no_interp = df[df["no_interp result"].astype(str).str.strip() != "timeout"]

    # === Extract and sort durations ===
    column_sql_solver = df_sql_solver["sqlsolver duration"].astype(float).sort_values().tolist()
    column__modified_sql_solver = df_modified_sql_solver["modified_sqlsolver duration"].astype(float).sort_values().tolist()
    column_cvc5_lia = df_cvc5_lia["cvc5 lia duration"].astype(float).sort_values().tolist()
    column_sls = df_sls["sls duration"].astype(float).sort_values().tolist()
    # column_normaliz = df_normaliz["lia normaliz duration"].astype(float).sort_values().tolist()
    column_unfold5 = df_unfold5["unfold5 duration"].astype(float).sort_values().tolist()
    column_no_interp = df_no_interp["no_interp duration"].astype(float).sort_values().tolist()

    # === Compute cumulative sums ===
    sql_solver_cum = np.cumsum(column_sql_solver)
    modified_sql_solver_cum = np.cumsum(column__modified_sql_solver)
    cvc5_cum = np.cumsum(column_cvc5_lia)
    sls_cum = np.cumsum(column_sls)
    # normaliz_cum = np.cumsum(column_normaliz)
    unfold5_cum = np.cumsum(column_unfold5)
    no_interp_cum = np.cumsum(column_no_interp)

    sql_solver_x = list(range(1, len(sql_solver_cum) + 1))
    modified_sql_solver_x = list(range(1, len(modified_sql_solver_cum) + 1))
    cvc5_x = list(range(1, len(cvc5_cum) + 1))
    sls_x = list(range(1, len(sls_cum) + 1))
    # normaliz_x = list(range(1, len(normaliz_cum) + 1))
    unfold5_x = list(range(1, len(unfold5_cum) + 1))
    no_interp_x = list(range(1, len(no_interp_cum) + 1))

    # === Plot ===
    plt.figure(figsize=(10, 6))
    plt.plot(sql_solver_cum, sql_solver_x, label="SQLSolver", linewidth=2)
    plt.plot(modified_sql_solver_cum, modified_sql_solver_x, label="Modified SQLSolver", linewidth=2)
    plt.plot(cvc5_cum, cvc5_x, label="cvc5", linewidth=2)
    plt.plot(sls_cum, sls_x, label="SLS-reachability (unfold-0)", linewidth=2)
    # plt.plot(normaliz_cum, normaliz_x, label="normaliz", linewidth=2)
    plt.plot(unfold5_cum, unfold5_x, label="SLS-reachability (unfold-5)", linewidth=2)
    plt.plot(no_interp_cum, no_interp_x, label="SLS-reachability (no-interpolation)", linewidth=2)

    plt.xlabel("Cumulative time (s)")
    plt.ylabel("Number of solved instances")
    plt.title("Cactus Plot: Solver Performance")
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
    plt.savefig(output1, dpi=300)
    plt.savefig(output2, dpi=300)


plot("comparison.csv", "cactus_plot.png", "/home/mudathir/all/paper-fmcad26-liastar/images/cactus_plot.png")
plot("comparison_speed.csv", "cactus_plot_speed.png", "/home/mudathir/all/paper-fmcad26-liastar/images/cactus_plot_speed.png")