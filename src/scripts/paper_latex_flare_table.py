"""

Script that produces a LaTeX table with the 
results of the flare finding and characterization.

"""

import paths
import pandas as pd

if __name__ == "__main__":

    # Load the data
    flare_table = pd.read_csv(paths.data / "PAPER_flare_table.csv")

    # Sort the data by orbital phase
    flare_table = flare_table.sort_values(by="orbital_phase", ascending=True)

    # Get ED with uncertainties in one expression
    flare_table[r"$ED$ [s]"] = flare_table.apply(lambda x: fr"${x.ED:.2f} \pm {x.ED_err:.2f}$",
                                                 axis=1)
    # Delete the now obsolete columns
    del flare_table["ED"]
    del flare_table["ED_err"]

    # Get 4 digits after decimal point for amplitude column
    flare_table["rel_amplitude"] = flare_table.apply(lambda x: fr"${x.rel_amplitude:.4f}$",
                                                     axis=1)

    # Get 4 digits after decimal point for tstart column
    flare_table["tstart"] = flare_table.apply(lambda x: fr"${x.tstart:.4f}$",
                                              axis=1)

    # Get 4 digits after decimal point for tstop column    
    flare_table["tstop"] = flare_table.apply(lambda x: fr"${x.tstop:.4f}$",
                                             axis=1)

    # Get 3 digits after decimal point for orbital phase column
    flare_table["orbital_phase"] = flare_table.apply(lambda x: fr"${x.orbital_phase:.3f}$",
                                                axis=1)

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