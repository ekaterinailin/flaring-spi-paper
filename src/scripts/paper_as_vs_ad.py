"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2023, MIT License

Script that generates a figure of AD test p-values vs. star-planet distance
minus Alfvén surface radius for the discussion of whether the AS is larger
than the planet's orbit.
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import paths

import adjustText as aT

if __name__ == "__main__":

    # read results
    df = pd.read_csv(paths.data / 'results.csv')

     # remove GJ 1061 because it does not have a rotation period
    df = df[df["ID"] != "GJ 1061"]

    # drop rows with TIC 67646988 and 236387002, the brown dwarfs
    df = df[df.TIC != "67646988" ]
    df = df[df.TIC != "236387002" ]

    # the old Kepler-411 instance
    df = df[df.TIC != "399954349(c)" ]

    # remove multiple stars
    df = df[df["multiple_star"].isnull()]

    # read AS
    AS = pd.read_csv(paths.data / 'AS_estimation.csv')

    # merge tables
    df = df.merge(AS, on='ID')

    # pick only valid values
    d = df[["ID", "a_au", 'a_au_err', 'AS_au', 'AS_au_max_error',
            'AS_au_min_error', 'mean', 'std']].dropna(how='any')

    print(d.shape)

    # plot
    plt.figure(figsize=(6.5,5))

    d["error_up"] = np.sqrt(d.a_au_err**2 + d.AS_au_max_error**2)
    d["error_low"] = np.sqrt(d.a_au_err**2 + d.AS_au_min_error**2)

    plt.errorbar(d.a_au -  d.AS_au, d["mean"], 
                xerr=[d.error_low, d.error_up], yerr = d["std"],
                fmt='d', color='olive',markersize=8, elinewidth=0.5)

    txts = []
    for i, row in d.iterrows():
        if (row['mean'] < 0.2) | (row['a_au'] - row['AS_au'] < -0.05):
            txts.append(plt.annotate(row.ID, (row.a_au - row.AS_au, row["mean"]),
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

    plt.savefig(paths.figures / 'PAPER_AS_vs_AD.png', dpi=300)