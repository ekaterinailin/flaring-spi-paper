"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that calculates the Spearman and Pearson correlation coefficients for
the tidal and magnetic interaction results.
"""

import pandas as pd
import numpy as np
import paths

from scipy.stats import spearmanr, pearsonr

if __name__ == "__main__":

    # read in the tidal results
    df = pd.read_csv(paths.data / "TIS_with_ADtests.csv")

    # calculate the Spearman and Pearson correlation coefficients
    for model in ["torque_conv", "tidal_disip_timescale", "grav_pert"]:
        d = df[[model, "mean"]]
        coeff = spearmanr(np.abs(d[model]), d["mean"])
        pcoeff = pearsonr(np.abs(d[model]), d["mean"])
        logcoeff = spearmanr(np.log10(np.abs(d[model])), np.log10(d["mean"]))
        plogcoeff = pearsonr(np.log10(np.abs(d[model])), np.log10(d["mean"]))
        print(model)
        print(coeff)
        print(logcoeff)
        print(pcoeff)
        print(plogcoeff)
        print("")

    # read magnetic SPI table
    df = pd.read_csv(paths.data / "results.csv")

    # select only the single stars
    singles = df[df.multiple_star.isnull()]

    # rename the column with the source of the rotation period
    singles = singles.rename(columns={"st_rotp_source":"st_rotp_bibkey"})

    # drop rows with TIC 67646988 and 236387002, the brown dwarfs
    singles = singles[singles.TIC != "67646988" ]
    singles = singles[singles.TIC != "236387002" ]

    # the old Kepler-411 instance
    singles = singles[singles.TIC != "399954349(c)" ]

    # GJ 1061 because rotation is unclear
    singles = singles[singles.TIC != "79611981" ]

    # calculate the Spearman and Pearson correlation coefficients
    for model in ["p_spi_sb_bp1_norm","p_spi_sb_bp0_norm",
                "p_spi_aw_bp1_norm","p_spi_aw_bp0_norm"]:
        
        d = df[[model, "mean"]].dropna(how="any")
        pcoeff = pearsonr(np.abs(d[model]), d["mean"])
        logcoeff = spearmanr(np.log10(np.abs(d[model])), np.log10(d["mean"]))
        plogcoeff = pearsonr(np.log10(np.abs(d[model])), np.log10(d["mean"]))
        print(model)
        print(coeff)
        print(logcoeff)
        print(pcoeff)
        print(plogcoeff)