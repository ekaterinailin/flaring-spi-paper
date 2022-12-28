"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that generates histograms of the orbital and rotation
period coherence times relative to the observing time span to
show that the orbital period is coherent enough for our analysis,
while the rotation period is not.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import paths

if __name__ == "__main__":

    # get matplotlib style
    plt.style.use(paths.scripts / 'paper.mplstyle')

    # read in flare table
    df = pd.read_csv(paths.data / "results.csv")

    # define the same bin for both rotation and orbit
    bins = np.logspace(-5.5, 2., 30)

    # plot the result and save the file
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(6, 9.5))

    # define the columns and labels
    cols = ["coherence_ratio_rotation", "coherence_ratio_orbit"]
    labels = ["rotation period", "orbital period"]

    # loop over the columns, labels, and axes
    for col, label, ax in list(zip(cols, labels, axes)):

        # plot the histogram
        ax.hist(df[col],
                bins=np.logspace(-5.5, 2., 30),
                facecolor="orange", edgecolor="maroon")
        
        # layout the x-axis
        ax.set_xscale("log")

        # set the labels
        l_ = (f"time span between first and last detected flare /"
            f"\n coherence time of {label}")
        ax.set_xlabel(l_, size=12)
        ax.set_ylabel("number of star-planet systems", size=12)

    # layout the figure
    plt.tight_layout()

    # save the figure
    plt.savefig(paths.figures / "PAPER_coherence_histogram.png", dpi=300)