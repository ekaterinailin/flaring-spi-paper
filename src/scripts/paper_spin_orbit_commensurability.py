"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that generates the spin-orbit commensurability plot for the paper.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import paths


def build_ratios_table(tol:float=1e-5)->dict:
    """
    Create a table of small integer ratios 
    with a tolerance used to determine if the ratio between two 
    periods is close to a small integer ratio.

    Parameters:
        tol (float): 
        The tolerance used to determine if the ratio between 
        the two periods is close to a small integer ratio.
        Default is 1e-5

    Returns:
        dict: A dictionary of ratios with the key as the ratio
        and value as a tuple of numerator and denominator
    """

    ratios = {}
    
    for i in range(1, int(np.sqrt(1/tol))):
        for j in range(1, int(np.sqrt(1/tol))):
            ratio = round(i/j, int(-np.log10(tol)))
            if ratio not in ratios:
                ratios[ratio] = (i,j)
    return ratios


def is_spin_orbit_commensurable(period1:float, period2:float,  ratios:dict, 
                                tol:float=1e-5,)->tuple:
    """
    Check for spin-orbit commensurability between two periods.
    Spin-orbit commensurability occurs when the ratio between the rotation period
    of a celestial body and its orbital period around another body is close to a 
    small integer ratio.

    Parameters:
    ----------
        period1 (float):
            The rotation period of a celestial body.
        period2 (float): 
            The orbital period around another body.
        tol (float): 
            The tolerance used to determine if the ratio between 
            the two periods is close to a small integer ratio.
            Default is 1e-5
        ratios (dict):
            A dictionary of ratios with the key as the ratio
            and value as a tuple of numerator and denominator


    Returns:
    -------
        tuple:  A tuple containing,
                A boolean value indicating whether the ratio is close to small integer ratio
                The closest ratio in the form of tuple (i,j) where i,j are small integers.
    """
    ratio = round(period1/period2, int(-np.log10(tol)))
    
    if ratio in ratios:
        sor = ratios[ratio]
        return (True, sor, np.abs((period1/period2-ratio)/ratio))
    else:
        closest_ratio = min(ratios, key=lambda x: abs(x-ratio))
        sor = ratios[closest_ratio]
        return (False, ratios[closest_ratio], np.abs((period1/period2-closest_ratio)/closest_ratio))

if __name__ == "__main__":

    # read in results table
    df = pd.read_csv(paths.data / "results.csv")


    # drop rows with TIC 67646988 and 236387002, the brown dwarfs
    df = df[df.TIC != "67646988" ]
    df = df[df.TIC != "236387002" ]

    # the old Kepler-411 instance
    df = df[df.TIC != "399954349(c)" ]

    # GJ 1061 because rotation is unclear
    df = df[df.TIC != "79611981" ]

    # pick only single systems
    df = df[df["multiple_star"].isnull()]

    # set tolerance to ratios with values <10 each
    tol = 0.01

    # build a table of small integer ratios
    ratios = build_ratios_table(tol=tol)
    
    res = df.apply(lambda x: is_spin_orbit_commensurable(x['st_rotp'], x['orbper_d'], 
            ratios, tol=tol), axis=1)


    df["spin_orbit_commensurable"] = res.apply(lambda x: x[0])
    df["closest_ratio_num"] = res.apply(lambda x: x[1][0])
    df["closest_ratio_den"] = res.apply(lambda x: x[1][1])
    df["ratio_error"] = res.apply(lambda x: x[2])


    # Color-code the points


    power_names = ["p_spi_sb_bp1_norm", "p_spi_sb_bp0_norm", 
                   "p_spi_aw_bp1_norm", "p_spi_aw_bp0_norm"]


    for power_name in power_names:

        # baseline color coding
        df["color"] = "blue"
        df["marker"] = "o"


        # label all that are expected with higher power than lowest for low p-values
        #  but SPI off
        cutoff = df.loc[df["mean"] < 0.2 , power_name].min()
        cond = ((df[power_name]>cutoff) & (df["mean"]>.2))
        df.loc[cond, "color"] = "red"
        df.loc[cond, "marker"] = "X"

        # label all that are expected with higher power than cutoff and SPI on
        cond = df["mean"] < .2
        df.loc[cond, "color"] = "k"
        df.loc[cond, "marker"] = "d"


        # Make plot
        fig, (ax2, ax1) = plt.subplots(nrows=2, ncols=1, figsize=(8,10.5))

        # plot each group
        for marker, group in df.groupby("marker"):
            ax1.scatter(group["ratio_error"], group["mean"],
                        color=group["color"], alpha=1., marker=marker, s=60)

        # annotate points with high expected power and SPI on
        for i, row in df.iterrows():
            if (row["mean"] < 2e-1):
                ax1.annotate(f"{row.ID} ({row.closest_ratio_den}:{row.closest_ratio_num})",
                            (row.ratio_error*1.1, row["mean"]*.95))

        # label axes
        ax1.set_xlabel("relative difference to closest spin-orbit commensurable ratio",
                fontsize=14)
        ax1.set_ylabel(r"$p$-value of AD test",
                fontsize=14)

        # set log scale
        ax1.set_xscale("log")
        ax1.set_yscale("log")
        # ax1.set_xlim(0,.1)

    
        # Corresponding AD test vs. SPI plot

        # plot each group
        for marker, group in df.groupby("marker"):
            ax2.errorbar(group[power_name], group["mean"], yerr=group["std"],
                        xerr=[group[power_name]-group[f"{power_name}_low"],
                            group[f"{power_name}_high"] - group[power_name]],
                        color=group["color"].values[0], alpha=1., fmt=marker )

        # define legend
        valuelegend = [Line2D([0], [0], marker='o', color='w',
                        markerfacecolor='b', markersize=10),
                        Line2D([0], [0], marker='X', color='w',
                        markerfacecolor='red', markersize=10),
                        Line2D([0], [0], marker='d', color='w',
                        markerfacecolor='black', markersize=10),]

        # # define legend labels
        valuelabels = [ r"low expected power",
                        r"high expected power / SPI off",
                        r"high expected power / SPI on"]

        # annotate points with high expected power and SPI on


        # plot legend
        ax2.legend(valuelegend, valuelabels, loc=3, fontsize=14, frameon=False)

        # label axes
        ax2.set_xlabel("$\sim$ expected power of magnetic star-planet interactions",
                fontsize=14)
        ax2.set_ylabel(r"$p$-value of AD test",
                fontsize=14)

        # set log scale
        ax2.set_xscale("log")
        ax2.set_yscale("log")

        plt.tight_layout()

        # save figure to figures folder
        fig.savefig(paths.figures / f"PAPER_spin_orbit_commensurable_{power_name}.png", dpi=300)


    # save table to data folder

    df.to_csv(paths.data / "results_spin_orbit_commensurable.csv", index=False)