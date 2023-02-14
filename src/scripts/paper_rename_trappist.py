"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that renames EPIC 200164267 to TRAPPIST-1, and drops Kepler-411(c) 
in the tables.

"""

import paths

import pandas as pd

if __name__ == "__main__":

    # read in flare table
    df = pd.read_csv(paths.data / "PAPER_flare_table.csv")

    # rename the star
    df.loc[df.ID == "EPIC 200164267", "ID"] = "TRAPPIST-1"

    # drop Kepler-411(c) from the flare table
    df = df[df.ID != "Kepler-411(c)"]

    # write to file
    df.to_csv(paths.data / "PAPER_flare_table.csv", index=False)

    # read in results table
    df = pd.read_csv(paths.data / "results.csv")

    # rename the star
    df.loc[df.ID == "EPIC 200164267", "ID"] = "TRAPPIST-1"

    # drop Kepler-411(c) from the results table
    df = df[df.ID != "Kepler-411(c)"]

    # write to file
    df.to_csv(paths.data / "results.csv", index=False)

    