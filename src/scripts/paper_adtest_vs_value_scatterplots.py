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
    onesigma = 0.3173
    twosigma = 0.0455
    threesigma = 0.0027
    
    # put them in a list
    sigmas = [onesigma, twosigma, threesigma]
    sigma_label = [r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"]

    return sigmas, sigma_label



def colorcode_dist(dist):
    """Define color code and symbol marker for rotation period.

    Parameters
    ----------
    dist : float
        Distance in pc.

    Returns
    -------
    color : str
        Color code.
    marker : str
        Symbol marker.
    """
    if dist < 50.:
        color = "green"
        symbol = "o"

    elif (dist >= 50.) & (dist < 100.):
        color = "blue"
        symbol = "x"

    elif (dist >= 100.) & (dist < 150.):
        color = "black"
        symbol = "d"

    else:
        color = "lightgrey"
        symbol = "s"

    return color, symbol


def colorcode_rossby(ro):
    """Define color code and symbol marker for rotation period.

    Parameters
    ----------
    ro : float
        Rossby number.

    Returns
    -------
    color : str
        Color code.
    marker : str
        Symbol marker.
    """
    if ro < 1e-2:
        color = "green"
        symbol = "o"

    elif (ro >= 1e-2) & (ro < 0.3):
        color = "blue"
        symbol = "x"

    elif (ro >= 0.3) & (ro < 1.):
        color = "black"
        symbol = "d"

    elif (ro >= 1.):
        color = "lightgrey"
        symbol = "s"

    return color, symbol

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


def colorcode_multiplicity(snum):
    """Define color code and symbol marker for rotation period.

    Parameters
    ----------
    snum : float
        Number of stars in the system.

    Returns
    -------
    color : str
        Color code.
    marker : str
        Symbol marker.
    """
    if snum == 1.:
        color = "green"
        symbol = "o"

    elif snum>1:
        color = "blue"
        symbol = "x"

    else:
        color = "lightgrey"
        symbol = "s"

    return color, symbol

def colorcode_Lx(lx):
    """Define color code and symbol marker for available X-ray luminosity.

    Parameters
    ----------
    lx : float
        X-ray luminosity in erg/s.

    Returns
    -------
    color : str
        Color code.
    marker : str
        Symbol marker.
    """
    if np.isnan(lx):
        color = "blue"
        symbol = "o"

    elif np.isfinite(lx):
        color = "green"
        symbol = "x"

    else:
        color = "lightgrey"
        symbol = "s"

    return color, symbol

def colorcode_B_G(bg):
    """Define color code and symbol marker for B_G.

    Parameters
    ----------
    bg : float
        Magnetic field strength in Gauss.

    Returns
    -------
    color : str
        Color code.
    marker : str
        Symbol marker.
    """
    if bg < 100.:
        color = "lightgrey"
        symbol = "s"

    elif 100 <= bg < 1000.:
        color = "blue"
        symbol = "x"

    elif 1000 <= bg < 2000.:
        color = "black"
        symbol = "d"

    elif bg >= 2000.:
        color = "green"
        symbol = "o"

    else:
        color = "r"
        symbol = "*"
    

    return color, symbol


def make_adtest_figure(df, value, valuelabel, legend, labels, ext, ax, leg=False,
                       fontsize=13):
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
    ext : str
        Extension for the figure name.
    ax : matplotlib.axes._subplots.AxesSubplot
        Axes to plot on.
    leg : bool
        Whether to plot the legend.
    fontsize : int
        Font size for the x and y labels.
    
    Returns
    -------
    .png figure in the figures folder

    """


    # get reference sigma values
    sigmas, sigma_labels = get_sigma_values()

    # pick value of TOI-540 as the threshold for labeling
    threshold = df[df.ID=="TOI-540"][value].values[0]


    data = df[df[value].notnull()]

    texts = []

    # plot the data
    for color, group in data.groupby("color"):

        # make the scatter plot
        x = group[value]
        xhigh = group[value + "_high"]
        xlow = group[value + "_low"]
        ax.errorbar(x, group["mean"], 
                        xerr=[x - xlow, xhigh - x],
                         yerr=group["std"],
                     fmt=".",markersize=1,
                     c="grey", alpha=1., lw=0.5, zorder=0)
        ax.scatter(x, group["mean"], marker=group["symbol"].iloc[0],
                    c=color, alpha=1., s=50, zorder=1)

        # # add the label to each star
        for star, row in group.iterrows():
            if ((row["mean"]<=.2) & (row[value]>=threshold)) | (row["ID"]=="KOI-12") | (row["ID"] == "TAP 26"):
                texts.append(ax.text(x=row[value], y=row["mean"], s=row["ID"],
                        fontsize=12, ha="right", va="top", rotation=0))

    # log scale
    ax.set_yscale("log")
    ax.set_xscale("log")

    # add sigma lines
    for sigma, label in list(zip(sigmas, sigma_labels)):
        ax.axhline(sigma, color="grey", linestyle="-.")
        ax.text(data[f"{value}_high"].max()*1.2, sigma, label, fontsize=15,
                color="k", verticalalignment="center")

    # labels
    ax.set_ylabel("p-value of AD test", fontsize=fontsize)
    ax.set_xlabel(valuelabel, fontsize=fontsize)

    # legend
    if leg == True:
        ax.legend(legend, labels, loc=(0, 0.08), fontsize=13)

    # limits
    ax.set_xlim(data[f"{value}_low"].min() * 0.85, data[f"{value}_high"].max() * 1.15)
    ax.set_ylim(2e-3, 1)

    # adjust label positions
    adjust_text(texts, force_text=(1.2, 2.2), force_static=(1,1), 
                arrowprops=dict(arrowstyle="-", color='k', lw=0.5), ax=ax)



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
            markerfacecolor='lightgrey', markersize=10),
            Line2D([0], [0], marker='o', color='w',
            markerfacecolor='blue', markersize=10),
            Line2D([0], [0], marker='X', color='w',
            markerfacecolor='green', markersize=10),

           ]


    # define legend labels
    labels = [r"$10 \leq P_{rot} < 15$ d",
            r"$P_{rot} \geq 15$ d",
            r"$P_{rot} < 10$ d",
            r"no $P_{rot}$",
            f"B from Ro from Reiners2022",
            f"B from X-ray luminosity from FP2022",
           ]


    # ------------------------------------------------------------


    # ------------------------------------------------------------
    # THE ACTUAL PLOTTING

    # read in results table
    df = pd.read_csv(paths.data / "results.csv")

    # remove GJ 1061 because it does not have a rotation period
    df = df[df["ID"] != "GJ 1061"]

    # drop rows with TIC 67646988 and 236387002, the brown dwarfs
    df = df[df.TIC != "67646988" ]
    df = df[df.TIC != "236387002" ]

    # the old Kepler-411 instance
    df = df[df.TIC != "399954349(c)" ]

    # remove multiple stars
    df = df[df["multiple_star"].isnull()]

    # FOUR SCENARIO PLOTS

    columns = ["p_spi_sb_bp1_erg_s", "p_spi_sb_bp0_erg_s",
              "p_spi_aw_bp1_erg_s", "p_spi_aw_bp0_erg_s"]
    xlabels = [r"$\sim$ $P_{\rm spi,sb}$ (stretch-and-break interaction with magnetized planet)",
              r"$\sim$ $P_{\rm spi,sb0}$  (stretch-and-break interaction with unmagnetized planet)",
              r"$\sim$ $P_{\rm spi,aw}$  (Alfvén wing interaction with magnetized planet)",
              r"$\sim$ $P_{\rm spi,aw0}$  (Alfvén wing interaction with unmagnetized planet)"]

    # ------------------------------------------------------------
    # DISTANCE
    # ------------------------------------------------------------

    # define the colors and symbols for the different distance bins
    df["color"], df["symbol"] = zip(*df.sy_dist.apply(colorcode_dist))
    
    valuelegend = [Line2D([0], [0], marker='o', color='w',
                   markerfacecolor='green', markersize=10),
                   Line2D([0], [0], marker='X', color='w',
                   markerfacecolor='blue', markersize=10),
                   Line2D([0], [0], marker='d', color='w',
                   markerfacecolor='black', markersize=10),
                   Line2D([0], [0], marker='s', color='w',
                   markerfacecolor='lightgrey', markersize=10),]

    valuelabels = [ "d < 50 pc","50 pc < d < 100 pc","100 pc < d < 150 pc","d > 150 pc",]

    # set up figure
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))

    # make one list of all axes
    axes = axes.flatten()

    for value, valuelabel, ax in list(zip(columns, xlabels, axes)):
        if value=="p_spi_sb_bp1_erg_s":
            leg = True
        else:
            leg = False
        make_adtest_figure(df, value, valuelabel, valuelegend, valuelabels, f"{value}_dist", ax, leg=leg)

    
    # layout the figure
    plt.tight_layout()

    # save the figure
    plt.savefig(paths.figures / f"PAPER_ADtest_dist.png", dpi=300)

    # ------------------------------------------------------------
    # MAGNETIC FIELD
    # ------------------------------------------------------------

    # define the colors and symbols for the different magnetic field bins
    df["color"], df["symbol"] = zip(*df.B_G.apply(colorcode_B_G))

    valuelegend = [ Line2D([0], [0], marker='s', color='w',
                     markerfacecolor='lightgrey', markersize=10),
                    Line2D([0], [0], marker='X', color='w',
                    markerfacecolor='blue', markersize=10),
                      Line2D([0], [0], marker='d', color='w',
                     markerfacecolor='k', markersize=10),
                    Line2D([0], [0], marker='o', color='w',
                     markerfacecolor='green', markersize=10)]

    valuelabels = ["B < 100 G",   "100 G < B < 1000 G", "1000 G < B < 2000 G", "B > 2000 G" ]

      # set up figure
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))

    # make one list of all axes
    axes = axes.flatten()

    for value, valuelabel, ax in list(zip(columns, xlabels, axes)):
        if value=="p_spi_sb_bp0_erg_s":
            leg = True
        else:
            leg = False
        make_adtest_figure(df, value, valuelabel, valuelegend, valuelabels, f"{value}_bp", ax, leg=leg)

    
    # layout the figure
    plt.tight_layout()

    # save the figure
    plt.savefig(paths.figures / f"PAPER_ADtest_bg.png", dpi=300)


    # ADD ONE PANEL AS THE MAIN PLOT
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8, 5))
    value = columns[1]
    valuelabel = xlabels[1]
    make_adtest_figure(df, value, valuelabel, valuelegend, valuelabels, f"{value}_bp", ax, leg=True)
    plt.tight_layout()
    plt.savefig(paths.figures / f"PAPER_ADtest_bg_main.png", dpi=300)

    # ADD THREE PANELS FOR THE REMAINING PLOTS
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(6.5, 13))
    axes = axes.flatten()

    for value, valuelabel, ax in list(zip(np.array(columns)[[0,2,3]], np.array(xlabels)[[0,2,3]], axes)):
        if value=="p_spi_sb_bp1_erg_s":
            leg = True
        else:
            leg = False
        make_adtest_figure(df, value, valuelabel, valuelegend, valuelabels, f"{value}_bp", ax, leg=leg, fontsize=11)

    plt.tight_layout()
    plt.savefig(paths.figures / f"PAPER_ADtest_bg_rest.png", dpi=300)


    # ------------------------------------------------------------
    # ROSSBY NUMBER
    # ------------------------------------------------------------

    # define the colors and symbols for the different distance bins
    df["color"], df["symbol"] = zip(*df.Ro.apply(colorcode_rossby))
    
    valuelegend = [Line2D([0], [0], marker='o', color='w',
                   markerfacecolor='green', markersize=10),
                   Line2D([0], [0], marker='X', color='w',
                   markerfacecolor='blue', markersize=10),
                   Line2D([0], [0], marker='d', color='w',
                   markerfacecolor='black', markersize=10),
                   Line2D([0], [0], marker='s', color='w',
                   markerfacecolor='lightgrey', markersize=10),]

    valuelabels = [ "Ro < .01","0.01 < Ro < 0.3","0.3 < Ro < 1","Ro > 1",]

    # set up figure
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(16, 10))

    # make one list of all axes
    axes = axes.flatten()

    for value, valuelabel, ax in list(zip(columns, xlabels, axes)):
        if value=="p_spi_sb_bp1_erg_s":
            leg = True
        else:
            leg = False
        make_adtest_figure(df, value, valuelabel, valuelegend, valuelabels, f"{value}_ro", ax, leg=leg)

    
    # layout the figure
    plt.tight_layout()

    # save the figure
    plt.savefig(paths.figures / f"PAPER_ADtest_Ro.png", dpi=300)

    # ------------------------------------------------------------
    # MULTIPICITY
    # ------------------------------------------------------------

    # # define the colors and symbols for the different multiplicity
    # df["color"], df["symbol"] = zip(*df.sy_snum.apply(colorcode_multiplicity))

    # valuelegend = [Line2D([0], [0], marker='X', color='w',
    #                markerfacecolor='blue', markersize=10),
    #                Line2D([0], [0], marker='o', color='w',
    #                markerfacecolor='green', markersize=10),
    #                Line2D([0], [0], marker='s', color='w',
    #                markerfacecolor='lightgrey', markersize=10)]

    # valuelabels = ["multiple star",
    #                "single star",
    #                "unknown multiplicity"]

    # for value, valuelabel in list(zip(columns, xlabels)):
    #     make_adtest_figure(df, value, valuelabel, valuelegend, valuelabels, f"{value}_multiplicity")

    # # ------------------------------------------------------------

