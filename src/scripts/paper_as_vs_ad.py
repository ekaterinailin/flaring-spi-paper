"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2023, MIT License

Script that generates a figure of AD test p-values vs. star-planet distance
minus Alfvén surface radius for the discussion of whether the AS is larger
than the planet's orbit.
"""


import pandas as pd
import matplotlib.pyplot as plt
import paths

import adjustText as aT

if __name__ == "__main__":

    # read results
    df = pd.read_csv(paths.data / 'results.csv')

    # read AS
    AS = pd.read_csv(paths.data / 'AS_estimation_table.csv')

    # merge tables
    df = df.merge(AS, on='ID')

    # pick only valid values
    d = df[["ID","a_au",'a_au_err','AS_AU','mean','std']].dropna(how='any')

    # plot
    plt.figure(figsize=(6.5,5))

    plt.errorbar(d.a_au -  d.AS_AU, d["mean"], 
                xerr=d.a_au_err, yerr = d["std"],
                fmt='d', color='olive',markersize=8, elinewidth=0.5)

    txts = []
    for i, row in d.iterrows():
        if (row['mean'] < 0.2) | (row['a_au'] - row['AS_AU'] < -0.05):
            txts.append(plt.annotate(row.ID, (row.a_au - row.AS_AU, row["mean"]),
                                    fontsize=12))

    # vertical dashed line at 0
    plt.axvline(0, color='k', linestyle='--', lw=2)

    # shade region where AS is larger than a
    plt.axvspan(0, -0.3, alpha=0.2, color='orange')

    # plt.xscale('log')
    plt.yscale('log')

    # adjust texts
    aT.adjust_text(txts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))

    plt.xlim(-0.28,0.22)
    plt.ylim(5e-3,1)

    plt.xlabel('planet-star distance - Alfvén surface radius [au]', fontsize=14)
    plt.ylabel('p-value of AD test', fontsize=14)

    plt.tight_layout()

    plt.savefig(paths.figures / 'paper_AS_vs_AD.png', dpi=300)