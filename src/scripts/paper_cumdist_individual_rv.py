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
    df = pd.read_csv(paths.data / "PAPER_flare_table.csv")

    # pick only real flares
    df = df[(~df.tstart.isnull()) & (df.orbital_phase==-1)]

    # only use the systems that appear in the results table
    res = pd.read_csv(paths.data / "results.csv")

    tics = res[(res.multiple_star.isnull()) & (res.multiple_star_source != "BD")]
    tics = tics.sort_values(by="number_of_flares", ascending=False).TIC.astype(str)

    tics = tics.values

    # make a plot for 15 panels
    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(14,11), sharex=True)

    # linearize the axes
    ax = [_1 for _0 in ax for _1 in _0]

    # create a subplot for each star
    for tic in tics:

        # print(g.shape)
        g = df[df.TIC.astype(str) == tic]
        print(tic, g.shape, len(ax))
        # pick only stars with more than 0 flares
        if ((g.shape[0]>3) & (len(ax)>0)):
            
            # pick an axis
            a = ax.pop()
            
            # gey the ID
            ID = g.ID.iloc[0]
            
            # if no ID, use TIC instead
            if str(ID)=="nan":
                print(ID)
                ID = f"TIC {g.TIC.iloc[0]}"

            # get the orbital period
            orbper = res[res.TIC.astype(str) == tic].orbper_d.values[0]
            
            # calculate the phases
            phases = g.tstart.values / orbper % 1.

            # sort the phases
            phases = np.sort(phases)
            
            # define the bins
            bins = np.linspace(0,1,len(phases))
    
            # plot the histogram
            a.hist(phases, bins=bins, histtype="step",
                cumulative=True,)
            
            # make a line for the legend
            line = Line2D([0], [0], color='w', linestyle='-', 
                            linewidth=1, alpha=0.)
            label = f"{ID}, {len(phases)} flares"

            # add the legend
            a.legend([line], [label], loc=(-.1,.87), fontsize=13)
            
            # plot a 1-1 line
            a.plot([0,1],[0,len(g)], linestyle="dotted")

            # set the limits
            a.set_xlim(0,1)

            # set the axis labels
            if len(ax) > 5:
                a.set_xlabel("orbital phase")
            a.set_ylabel("number of flares")

    # layout the figure
    plt.tight_layout(h_pad=0.1)

    # make sure y-axis labels are visible
    plt.subplots_adjust(left=0.07, right=0.97, top=0.97, bottom=0.05)


    # save the figure
    plt.savefig(paths.figures / "PAPER_flares_phase_hist_rv.png", dpi=300)
