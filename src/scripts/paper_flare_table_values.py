"""

Script that produces a LaTeX table with the 
results of the flare finding and characterization.

"""

import paths
import pandas as pd

if __name__ == "__main__":

    # Load the data
    flare_table = pd.read_csv(paths.data / "PAPER_flare_table.csv")

    # define total number of flares and write to file
    total_number_of_flares = flare_table[~flare_table["tstart"].isnull()].shape[0]
    print("Total number of flares: ", total_number_of_flares)

    with open(paths.output / "PAPER_total_number_of_flares.txt", "w") as f:
        f.write(f"{total_number_of_flares}")


    # total number of systems with flares
    total_number_of_systems_with_flares = flare_table[~flare_table["tstart"].isnull()]["TIC"].unique().shape[0]
    print("Total number of systems with flares: ", total_number_of_systems_with_flares)

    with open(paths.output / "PAPER_total_number_of_systems_with_flares.txt", "w") as f:
        f.write(f"{total_number_of_systems_with_flares}")

    # table contains only systems that flare
    assert flare_table["TIC"].unique().shape[0] == total_number_of_systems_with_flares

    # total number of light curves searched
    total_number_of_light_curves = flare_table.groupby(["TIC", "quarter_or_sector"]).size().shape[0]
    print("Total number of light curves: ", total_number_of_light_curves)

    with open(paths.output / "PAPER_total_number_of_light_curves.txt", "w") as f:
        f.write(f"{total_number_of_light_curves}")

    # total number of light curves without flares
    light_curves_without_flares = flare_table[flare_table["tstart"].isnull()].groupby(["TIC", "quarter_or_sector"]).size().shape[0]
    print("Total number of light curves without flares: ", light_curves_without_flares)
 
    assert flare_table.shape[0] == total_number_of_flares + light_curves_without_flares
