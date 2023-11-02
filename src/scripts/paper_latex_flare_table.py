"""

Script that produces a LaTeX table with the 
results of the flare finding and characterization.

"""

import paths
import pandas as pd

from stringmanipulation import get_err_string

if __name__ == "__main__":

    # Load the data
    flare_table = pd.read_csv(paths.data / "PAPER_flare_table.csv")

    # Sort the data by orbital phase
    flare_table = flare_table.sort_values(by="tstart", ascending=True)

    # remove duplicates 
    # Group by TIC and quarter_or_sector, then by timestamp and total_time_observed_in_lc_days, and remove all but first in each group
    for l, g in flare_table.groupby(['TIC', 'quarter_or_sector']):
        grouped = g.groupby(['timestamp', 'total_time_observed_in_lc_days'])

        # now keep only the first group
        flare_table = flare_table.drop(grouped.tail(len(grouped)-1).index)

    print(flare_table[flare_table.ID == "HIP 67522"])

    flare_table.to_csv(paths.data / "zenodo/Table_2_flares.csv", index=False)

    # add text to the top of the written table with explanations of each column
    top_text = ("# TIC and ID, star designations\n"
                "# mission, TESS or Kepler\n"
                "# quarter_or_sector, TESS sector or Kepler quarter\n"
                "# timestamp, date when light curve was downloaded and analysed\n"
                "# total_time_observed_in_lc_days, total time observed in this light curve, calculated by summing all valid data points times the cadence\n"
                "# orbital_phase, orbital phase of the flare\n"
                "# orbital_phase_err, uncertainty on the orbital phase, derived only for the stars in the final sample\n"
                "# rel_amplitude, relative amplitude of the flare\n"
                "# rel_amplitude_err, uncertainty on the relative amplitude\n"
                "# tstart, start time of the flare\n"
                "# tstop, stop time of the flare\n"
                "# ED, equivalent duration of the flare in s\n"
                "# ED_err, uncertainty on the equivalent duration\n"
                "# abs_tstart, flare start time in BJD instead of with Kepler/TESS offsets\n")
    
    # add the top text to the top of the table in the zenodo folder
    with open(paths.data / "zenodo/Table_2_flares.csv", "r") as f:
        lines = f.readlines()
    with open(paths.data / "zenodo/Table_2_flares.csv", "w") as f:
        f.write(top_text)
        f.writelines(lines)


    # Get ED with uncertainties in one expression
    # flare_table[r"$ED$ [s]"] = flare_table.apply(lambda x: fr"${x.ED:.2f} \pm {x.ED_err:.2f}$",
    #                                              axis=1)
 

    # Get 4 digits after decimal point for amplitude column
    flare_table["rel_amplitude"] = flare_table.apply(lambda x: fr"${x.rel_amplitude:.4f}$",
                                                     axis=1)



    # Get 4 digits after decimal point for tstart column
    flare_table["tstart"] = flare_table.apply(lambda x: fr"${x.tstart:.4f}$",
                                              axis=1)

    # Get 4 digits after decimal point for tstop column    
    flare_table["tstop"] = flare_table.apply(lambda x: fr"${x.tstop:.4f}$",
                                             axis=1)

    flare_table["orbital_phase"] = get_err_string(flare_table,"orbital_phase","orbital_phase_err")
    flare_table[r"$ED$ [s]"] = get_err_string(flare_table,"ED","ED_err")

    # Delete the now obsolete columns
    del flare_table["orbital_phase_err"]
    del flare_table["ED"]
    del flare_table["ED_err"]

    # Rename columns to be the same as in the AU Mic paper
    flare_table = flare_table.rename(index=str,
                                columns={"quarter_or_sector": "Qua./Sec.",
                                         "orbital_phase": r"orb. phase",
                                         "rel_amplitude":r"$a$",
                                         "tstart":r"$t_s$ [BKJD/BTJD]",
                                         "tstop":r"$t_f$ [BKJD/BTJD]",
                                         })

    # Pick the final columns to include in the right order
    final_columns = ["TIC", "ID", "mission", "Qua./Sec.",
                    r"$t_s$ [BKJD/BTJD]", r"$t_f$ [BKJD/BTJD]", 
                    "orb. phase", r"$a$", r"$ED$ [s]"]
    flare_table = flare_table[final_columns]

    # Convert the dataframe to a LaTeX table
    c = "c" * (len(final_columns) - 1)
    stri = flare_table.head(20).to_latex(index=False,escape=False,
                                         column_format=f"l{c}")

    # Make some layout adjustments
    stri = stri.replace("\\toprule","\hline")
    stri = stri.replace("\\midrule","\hline")
    stri = stri.replace("{}","\hline")
    stri = stri.replace("\\bottomrule","\hline\n" )
    stri = stri.replace("NaN","   " )

    # Write the table to a file
    with(open(paths.output / "flare_table.tex","w")) as f:
        f.write(stri)