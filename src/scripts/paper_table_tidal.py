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

def round_to_1(x):
    if x == 0:
        return 0
    elif np.isnan(x):
        return np.nan
    else:
        return np.round(x, -int(np.floor(np.log10(np.abs(x)))))
    

def g(row, col, oneerr=False):
        """Converts a row of a dataframe to a latex formatted string.
        
        Parameters
        ----------
        row : pandas.Series
            Row of a dataframe.
        oneerr : bool, optional
            If True, only one error is shown. The default is False.

        Returns
        -------
        str
            Latex formatted string.
        """

        try:
            v = np.min([abs(row[col[0]]),abs(row[col[1]]),abs(row[col[2]])])
            n  = -int(np.floor(np.log10(np.abs(v))))
         
        except:
            n = 1
     
        if n < 0:
            # convert values in row to int
            

            if oneerr:
                for c in col[:2]:
                    row[c] = int(row[c])
                return f"${np.round(row[col[0]], n):d} [{np.round(row[col[2]], n):d}]$"

            else:
               for c in col[:3]:
                    row[c] = int(row[c])
               return (f"${np.round(row[col[0]], n):d}" +
                        r"^{" +
                        f"{np.round(row[col[1]], n):d}" +
                        r"}_{" +
                        f"{np.round(row[col[2]], n):d}" +
                        r"}$")
        else:
            return (f"${row[col[0]]:.{n}f}" + 
                        r"^{" + 
                        f"{row[col[1]]:.{n}f}" + 
                        r"}_{" + 
                        f" {row[col[2]]:.{n}f}" + 
                        r"}$") 
    



if __name__ == "__main__":

    # read in the tidal results
    df = pd.read_csv(paths.data / "TIS_with_ADtests.csv")

    # sort by p-value
    df = df.sort_values(by="mean", ascending=False)

    # take absolute value of pl_bmassjerr2
    # df.M_pl_low_err = np.abs(df.M_pl_low_err)

    # take absolute value of st_masserr2
    # df.M_star_low_err = np.abs(df.M_star_low_err)

    # take absolute value of torque_conv_up_err and torque_conv_low_err
    # df.torque_conv_up_err = np.abs(df.torque_conv_up_err)
    # df.torque_conv_low_err = np.abs(df.torque_conv_low_err)

    # convert to latex readable entries 
    new_cols =  [r"$M_*$ [$M_\odot$]",
                r"$M_p$ [$M_\oplus$]",
                r"log$_{10} 10^{-8} \Delta g / g$",
                r"log$_{10} \tau_{\rm tide}$ [yr]",
                r"$10^{-20} \frac{\partial L_{conv}}{\partial t}$"
                r" $\left[M_\odot \left(\frac{km}{s}\right)^2\right]$",
                ]

    # convert "grav_pert",  "tidal_disip_timescale", "torque_conv" and errors to log10
    df["grav_pert"] = np.log10(df["grav_pert"] * 1e8)
    df["grav_pert_up_err"] = np.log10(df["grav_pert_up_err"] * 1e8)
    df["grav_pert_low_err"] = np.log10(df["grav_pert_low_err"] * 1e8)
    df["tidal_disip_timescale"] = np.log10(df["tidal_disip_timescale"])
    df["tidal_disip_timescale_up_err"] = np.log10(df["tidal_disip_timescale_up_err"] )
    df["tidal_disip_timescale_low_err"] = - np.log10(df["tidal_disip_timescale_low_err"] )
    df["torque_conv"] = df["torque_conv"] * 1e20
    df["torque_conv_up_err"] = df["torque_conv_up_err"] * 1e20
    df["torque_conv_low_err"] = - df["torque_conv_low_err"] * 1e20

    # multiply M_pl and errors by 317.907 to get Earth masses
    df["M_pl"] = df["M_pl"] * 317.907
    df["M_pl_up_err"] = df["M_pl_up_err"] * 317.907
    df["M_pl_low_err"] = df["M_pl_low_err"] * 317.907

   
    old_cols = ["M_star", "M_pl", "grav_pert", 
                "tidal_disip_timescale", "torque_conv"]


    for ocol, ncol in zip(old_cols, new_cols):
        print(ncol)
        col = [ocol, ocol + "_up_err", ocol + "_low_err"]

        df[ncol] = df.apply(g, axis=1, args=(col,))

    

    g = lambda row: f"{row['mean']:.2f} [{row['std']:.2f}]"  
    df[r"$p$-value"] = df.apply(g, axis=1)

    print(df)

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

