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
    df = df[df.orbital_phase != -1]

    # get the 15 stars with the most flares as a sorted list
    tics = df.groupby("TIC").count().sort_values("ED", ascending=False)
    tics = tics.head(15).reset_index().TIC.values

    # get the subsample of most active stars
    new_df = df[df.TIC.isin(tics)]

    # defined categorical index for tics
    new_df['TIC'] = pd.Categorical(new_df['TIC'], tics)

    # sort by new categorical index
    new_df = new_df.sort_values("TIC", ascending=False)

    # make a plot for 15 panels
    fig, ax = plt.subplots(nrows=5, ncols=3, figsize=(14,18))

    # linearize the axes
    ax = [_1 for _0 in ax for _1 in _0]

    # create a subplot for each star
    for i, g in new_df.groupby("TIC"):
        # pick only stars with more than 8 flares
        if ((g.shape[0]>8) & (len(ax)>0)):
            
            # pick an axis
            a = ax.pop()
            
            # gey the ID
            ID = g.ID.iloc[0]
            
            # if no ID, use TIC instead
            if str(ID)=="nan":
                print(ID)
                ID = f"TIC {g.TIC.iloc[0]}"

            # ge the phases
            phases = g.orbital_phase.sort_values(ascending=True).values
        
            # define the bins
            bins = np.linspace(0,1,len(phases))
    
            # plot the histogram
            a.hist(phases, bins=bins, histtype="step",
                cumulative=True,);
            
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
            a.set_xlabel("orbital phase")
            a.set_ylabel("number of flares")

    # layout the figure
    plt.tight_layout()

    # save the figure
    plt.savefig(paths.figures / "PAPER_flares_phase_hist.png", dpi=300)
