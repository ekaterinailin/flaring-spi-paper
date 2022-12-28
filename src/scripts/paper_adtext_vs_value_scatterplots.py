"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that generates the main figure of the paper, showing the
AD test results for the orbital period and compares them to the
expected values for the power of SPI (Lanza 2012), with and without
planetary magnetic fields, and also vs the X-ray luminosity.
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from adjustText import adjust_text

import paths


def get_sigma_values():
    """Define the sigma values."""

    # define sigma values
    onesigma = 1 - .342*2
    twosigma = 1 - .342*2 - .136*2
    threesigma = 1 - .342*2 - .136*2 - .021*2
    
    # put them in a list
    sigmas = [onesigma, twosigma, threesigma]
    sigma_label = [r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"]

    return sigmas, sigma_label


def colorcode_rotation(st_rotp):
    """Define color code and symbol marker for rotation period.

    Parameters
    ----------
    st_rotp : float
        Rotation period in days.

    Returns
    -------
    color : str
        Color code.
    marker : str
        Symbol marker.
    """
    if st_rotp < 10.:
        color = "green"
        symbol = "o"

    elif (st_rotp >= 10.) & (st_rotp < 15.):
        color = "blue"
        symbol = "x"

    elif (st_rotp >= 15.):
        color = "black"
        symbol = "d"

    else:
        color = "lightgrey"
        symbol = "s"

    return color, symbol



def make_adtest_figure(df, value, valuelabel, legend, labels):
    """Create an AD test vs. value figure.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Results table.
    value : str
        Column name of the value to plot.
    valuelabel : str
        Label for the value to go on the x-axis.
    legend : list
        List of legend elements.
    labels : list
        List of legend labels.
    
    Returns
    -------
    .png figure in the figures folder

    """


    # get reference sigma values
    sigmas, sigma_labels = get_sigma_values()

    # set up figure
    fig, ax = plt.subplots(figsize=(10, 6.5))

    data = df[df[value].notnull()]

    texts = []

    # plot the data
    for color, group in data.groupby("color"):

        # make the scatter plot
        plt.scatter(group[value], group["mean"], marker=group["symbol"].iloc[0],
                    c=color, s=50., alpha=1.)

        # add the label to each star
        for star, row in group.iterrows():
            texts.append(plt.text(x=row[value], y=row["mean"], s=row["ID"],
                        fontsize=11, ha="right", va="top", rotation=0))

    # log scale
    plt.yscale("log")
    plt.xscale("log")

    # add sigma lines
    for sigma, label in list(zip(sigmas, sigma_labels)):
        plt.axhline(sigma, color="grey", linestyle="-.")
        plt.text(data[value].max()*1.2, sigma, label, fontsize=15,
                color="k", verticalalignment="center")

    # labels
    plt.ylabel("p-value of AD test")
    plt.xlabel(valuelabel)

    # legend
    plt.legend(legend, labels, loc=(0, 0.07), fontsize=15)

    # limits
    plt.xlim(data[value].min() * 0.85, data[value].max() * 1.15)
    plt.ylim(1.5e-3, 1)

    # adjust label positions
    adjust_text(texts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))

    # layout the figure
    plt.tight_layout()

    # save the figure
    plt.savefig(paths.figures / f"PAPER_ADtest_vs_{value}.png", dpi=300)


if __name__ == "__main__":


    # ------------------------------------------------------------
    # PLOT SETTINGS

    # get matplotlib style
    plt.style.use(paths.scripts / 'paper.mplstyle')


    # define legend elements
    legend = [Line2D([0], [0], marker='X', color='w',
            markerfacecolor='blue', markersize=10),
            Line2D([0], [0], marker='d', color='w',
            markerfacecolor='black', markersize=10),
            Line2D([0], [0], marker='o', color='w',
            markerfacecolor='green', markersize=10),
            Line2D([0], [0], marker='s', color='w',
            markerfacecolor='lightgrey', markersize=10)]

    # define legend labels
    labels = [r"$10 \leq P_{rot} < 15$ d",
            r"$P_{rot} \geq 15$ d",
            r"$P_{rot} < 10$ d",
            r"no $P_{rot}$"]

    # ------------------------------------------------------------


    # ------------------------------------------------------------
    # THE ACTUAL PLOTTING

    # read in results table
    df = pd.read_csv(paths.data / "results.csv")

    # define the colors and symbols for the different rotation periods
    df["color"], df["symbol"] = zip(*df.st_rotp.apply(colorcode_rotation))


    # ------------------------------------------------------------
    # P-VALUE VS. P_SPI with Bp=1G

    value = "p_spi_erg_s"
    valuelabel = "P$_{SPI}$ [erg/s]  @ B$_p$=1G"
    valuelegend = legend[1:3]
    valuelabels = labels[1:3]

    make_adtest_figure(df, value, valuelabel, valuelegend, valuelabels)

    # ------------------------------------------------------------
    # P-VALUE VS. P_SPI with Bp=0G

    value = "p_spi_erg_s_bp0"
    valuelabel = "P$_{SPI}$ [erg/s] @ B$_p$=0G"
    valuelegend = legend[1:3]
    valuelabels = labels[1:3]

    make_adtest_figure(df, value, valuelabel, valuelegend, valuelabels)

    # ------------------------------------------------------------
    # P-VALUE VS. L_X

    value = "xray_flux_erg_s"
    valuelabel = r"$L_X$ [erg/s]"

    valuelegend = legend[1:]
    valuelabels = labels[1:]


    make_adtest_figure(df, value, valuelabel,  valuelegend, valuelabels)

    # ------------------------------------------------------------
