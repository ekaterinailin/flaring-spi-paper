"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that generates the tidal interaction of the paper, showing stellar and 
planetary mass which are necessary for analysis (and producing a string of 
references for the footnote), and 2. derived interaction, and AD test results 
for the Porb/2 (i.e., in phase with tidal bulges). 
"""

import pandas as pd
import numpy as np
import paths



if __name__ == "__main__":

    # read in the tidal results
    df = pd.read_csv(paths.data / "TIS_with_ADtests.csv")

    # sort by p-value
    df = df.sort_values(by="mean", ascending=False)

    # take absolute value of pl_bmassjerr2
    df.M_pl_low_err = np.abs(df.M_pl_low_err)

    # take absolute value of st_masserr2
    df.M_star_low_err = np.abs(df.M_star_low_err)

    # take absolute value of torque_conv_up_err and torque_conv_low_err
    df.torque_conv_up_err = np.abs(df.torque_conv_up_err)
    df.torque_conv_low_err = np.abs(df.torque_conv_low_err)

    # convert to latex readable entries 
    new_cols =  [r"$M_*$ [$M_\odot$]",
                r"$M_p$ [$M_\oplus$]",
                r"$10^{-8} \Delta g / g$",
                r"$\tau_{\rm tide}$ [Gyr]",
                r"$10^{-20} \frac{\partial L_{conv}}{\partial t}$"
                r" $\left[M_\odot \left(\frac{km}{s}\right)^2\right]$",
                ]

    factor = [1., 317.907, 1e8, 1e-8, 1e20, 1]
    n = [2, 1, 2, 1, 1, 3]
    fs = ["f", "f", "f", "e", "e", "f"]
    old_cols = ["M_star", "M_pl", "grav_pert", 
                "tidal_disip_timescale", "torque_conv"]


    for ocol, fac, n, f,  ncol in zip(old_cols, factor, n, fs, new_cols):
        df[ncol] = df.apply(lambda row: f"${row[ocol] * fac:.{n}{f}}" + 
                                        r"^{" + 
                                        f"{row[ocol + '_up_err'] * fac:.{n}{f}}" + 
                                        r"}_{" + 
                                        f" {row[ocol + '_low_err'] * fac:.{n}{f}}" + 
                                        r"}$", 
                                        axis=1)
    

    g = lambda row: f"{row['mean']:.2f} [{row['std']:.2f}]"  
    df[r"$p$-value"] = df.apply(g, axis=1)

    # add ID column and p-value column
    new_cols.insert(0, "ID")
    new_cols.append(r"$p$-value")


    # Get all bibkeys from singles table
    bibkeys = df.st_mass_bibkey.dropna().unique()
    bibkeys = np.append(bibkeys, df.pl_bmassj_bibkey.dropna().unique())

    # enumerate the bibkeys
    bibkeys = np.unique(bibkeys)

    # make a dictionary with the bibkeys and the corresponding index
    bibkeys = {bibkeys[i]:i+1 for i in range(len(bibkeys))}

    # add references
    df[r"ref. $M_*$"] = df.st_mass_bibkey.apply(lambda x: bibkeys[x])
    df[r"ref. $M_p$"] = df.pl_bmassj_bibkey.apply(lambda x: bibkeys[x])

    # add reference columns to new_cols
    new_cols.append(r"ref. $M_*$")
    new_cols.append(r"ref. $M_p$")


    # convert to latex
    string = df[new_cols].to_latex(index=False, escape=False,
                                    column_format="lllllllcc")

    string = string.replace(r"$nan^{nan}_{nan}$",r"--")
    string = string.replace(r"nan",r"-")
    string = string.replace(r"NaN",r"-") 
    string = string.replace("e+00",r"")
    string = string.replace("e-0",r"\text{e-}")
    string = string.replace("e+0",r"\text{e}")
    string = string.replace("midrule","hline")
    string = string.replace("toprule","hline")
    string = string.replace("bottomrule","hline")

    # write to file
    path = paths.output / f"table_tidal.tex"
    print("Write to file: ", path)

    with open(path, "w") as f:
        f.write(string)


    # generate a bibkey string to put in the footnote of the tex table
    bibstring = ""
    for key in bibkeys.keys():
        bibstring += "(" + str(bibkeys[key]) + ") \citet{" + key + "}, "


    # write the bibstring to a file
    path = paths.output / "table_tidal_bibstring.tex"
    print("Write footnote list to file: ", path)

    with open(path, "w") as f:
        f.write(bibstring)

