"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that generates the individual cumulative distribution 
plot for the paper using the final flare table.
"""

import paths

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


if __name__ == "__main__":

    # get matplotlib style
    plt.style.use(paths.scripts / 'paper.mplstyle')

    # read in flare table
    flares = pd.read_csv(paths.data / "PAPER_flare_table.csv")

    # pick only real flares
    flares = flares[flares.orbital_phase != -1]

    # only use the systems that appear in the results table
    tics = pd.read_csv(paths.data / "results.csv")

    # remove old Kepler-411 instance
    tics = tics[tics.TIC != '399954349(c)']

    # remove GJ 1061 because it does not have a rotation period
    tics = tics[tics["ID"] != "GJ 1061"]

    # drop rows with TIC 67646988 and 236387002, the brown dwarfs
    tics = tics[tics.TIC != "67646988" ]
    tics = tics[tics.TIC != "236387002" ]


    tics = tics[(tics.multiple_star.isnull()) & (tics.multiple_star_source != "BD")]
    tics = tics.sort_values(by="number_of_flares", ascending=False)


    # Add the number of flares to the TICs
    n_flares = []
    for tic in tics.TIC:
        n_flares.append(pd.read_csv(paths.data / f"TIC_{tic}_cumhist.csv").shape[0])
    
    # sort the TICs by the number of flares
    tics["n_flares"] = n_flares
    tics = tics.sort_values(by="n_flares", ascending=False)

    # make a plot for 15 panels
    fig, ax = plt.subplots(nrows=6, ncols=3, figsize=(14,17), sharex=True)

    # linearize the axes
    ax = [_1 for _0 in ax for _1 in _0]
    ax = ax[::-1]

    # create a subplot for each star
    for id_, row in tics.iterrows():

        # get the orbital phases
        phases = flares[flares.TIC.astype(str) == str(row.TIC)].orbital_phase.values

        if (len(phases) > 2) & (len(ax) > 0):
            a = ax.pop()

            # read in file with phase distribution
            df = pd.read_csv(paths.data / f"TIC_{row.TIC}_cumhist.csv")
            
            # plot the distribution
            a.plot(df.p, df.f, color="blue", linewidth=1.5)

            # plot the flares
            # sort the phases
            phases = np.sort(phases)
            print(len(phases))
            # plot the histogram
            hist = np.cumsum(np.ones_like(phases))
            hist = hist/hist[-1]
            # insert 1 and 0 at the beginning and the end
            hist = np.append(hist, 1)
            hist = np.insert(hist, 0, 0)
            phases = np.append(phases, 1)
            phases = np.insert(phases, 0, 0)
            print(phases)
            a.plot(phases, hist, color="k", linewidth=1.5)

            # make a line for the legend
            line = Line2D([0], [0], color='w', linestyle='-', 
                            linewidth=1, alpha=0.)
            label = f"{row.ID}, {len(phases)-2} flares"

            # add the legend
            a.legend([line], [label], loc=(-.1,.87), fontsize=13)
            
            # plot a 1-1 line
            a.plot([0,1],[0,1], linestyle="dotted")

            # set the limits
            a.set_xlim(0,1)

            # set the axis labels
            if len(ax) <3:
                a.set_xlabel("orbital phase")
            a.set_ylabel("number of flares")

    # layout the figure
    plt.tight_layout(h_pad=0.1)

    # make sure y-axis labels are visible
    plt.subplots_adjust(left=0.07, right=0.99, top=0.99, bottom=0.03)


    # save the figure
    plt.savefig(paths.figures / "PAPER_flares_phase_hist_transiting.png", dpi=300)
