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
    flares = flares[(~flares.tstart.isnull()) & (flares.orbital_phase==-1)]

    # only use the systems that appear in the results table
    res = pd.read_csv(paths.data / "results.csv")

    tics = res[(res.multiple_star.isnull()) & (res.multiple_star_source != "BD") & (res.TIC != "399954349(c)")]
    tics = tics.sort_values(by="number_of_flares", ascending=False).TIC.astype(str)

    tics = tics.values

    # Add the number of flares to the TICs
    n_flares = []
    for tic in tics:
        n_flares.append(pd.read_csv(paths.data / f"TIC_{tic}_cumhist.csv").shape[0])
    
    # sort the TICs by the number of flares
    tics = [x for _,x in sorted(zip(n_flares, tics), reverse=True)]

    # make a plot for 15 panels
    fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(14,9.5), sharex=True)

    # linearize the axes
    ax = [_1 for _0 in ax for _1 in _0]
    ax = ax[::-1]

    # create a subplot for each star
    for tic in tics:

        # print(g.shape)
        g = flares[(flares.TIC.astype(str) == tic)]
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

            # read in file with phase distribution
            df = pd.read_csv(paths.data / f"TIC_{tic}_cumhist.csv")
            
            # plot the distribution
            a.plot(df.p, df.f, color="blue", linewidth=1.5)


            # get the orbital period
            orbper = res[res.TIC.astype(str) == tic].orbper_d.values[0]
            
            # calculate the phases
            phases = g.tstart.values / orbper % 1.

            # sort the phases
            phases = np.sort(phases)
            
            # plot the histogram
            hist = np.cumsum(np.ones_like(phases))
            hist = hist/hist[-1]
            # insert 1 and 0 at the beginning and the end
            hist = np.append(hist, 1)
            hist = np.insert(hist, 0, 0)
            phases = np.append(phases, 1)
            phases = np.insert(phases, 0, 0)
           
            a.plot(phases, hist, color="k", linewidth=1.5)

            # make a line for the legend
            line = Line2D([0], [0], color='w', linestyle='-', 
                            linewidth=1, alpha=0.)
            label = f"{ID}, {len(phases)-2} flares"

            # add the legend
            a.legend([line], [label], loc=(-.1,.85), fontsize=13)
            
            # plot a 1-1 line
            a.plot([0,1],[0,1], linestyle="dotted")

            # set the limits
            a.set_xlim(0,1)

            # set the axis labels
            if len(ax) <5:
                a.set_xlabel("orbital phase")
            
            a.set_ylabel("fraction of flares")

    if len(ax) > 0:
        for a in ax:
            a.remove()

    # layout the figure
    plt.tight_layout(h_pad=0.1)

    # make sure y-axis labels are visible
    plt.subplots_adjust(left=0.07, right=0.97, top=0.97, bottom=0.07)


    # save the figure
    plt.savefig(paths.figures / "PAPER_flares_phase_hist_rv.png", dpi=300)
