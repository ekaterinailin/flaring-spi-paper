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
     
        if n==0:
            n=1
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

    # take neg value of st_masserr2
    df.M_star_low_err = - df.M_star_low_err

    # take neg value of pl_bmassjerr2
    df.M_pl_low_err = - df.M_pl_low_err

    dfz = df.copy()

    # select columns to go on zenodo
    cols = ["TIC", "ID", "M_star", "M_star_up_err", "M_star_low_err",
            "M_pl", "M_pl_up_err", "M_pl_low_err",	"grav_pert", 
            "grav_pert_low_err", "grav_pert_up_err", "tidal_disip_timescale",
            "tidal_disip_timescale_up_err", "tidal_disip_timescale_low_err",
            "torque_conv", "torque_conv_up_err", "torque_conv_low_err", "mean", "std"]

    # save table to file in the zenodo folder
    dfz[cols].to_csv(paths.data / "zenodo/Table_4_tidal_interaction.csv", index=False)

    # add text to the top of the written table with explanations of each column
    top_text = ("# TIC and ID, star designations\n"
                "# M_star, stellar mass in solar masses\n"
                "# M_star_up_err, upper uncertainty on the stellar mass\n"
                "# M_star_low_err, lower uncertainty on the stellar mass\n"
                "# M_pl, planetary mass in Jupiter masses\n"
                "# M_pl_up_err, upper uncertainty on the planetary mass\n"
                "# M_pl_low_err, lower uncertainty on the planetary mass\n"
                "# grav_pert, gravitational perturbation\n"
                "# grav_pert_low_err, lower uncertainty on the gravitational perturbation\n"
                "# grav_pert_up_err, upper uncertainty on the gravitational perturbation\n"
                "# tidal_disip_timescale, tidal dissipation timescale in years\n"
                "# tidal_disip_timescale_up_err, upper uncertainty on the tidal dissipation timescale\n"
                "# tidal_disip_timescale_low_err, lower uncertainty on the tidal dissipation timescale\n"
                "# torque_conv, convective torque in solar masses x (km/s)^2\n"
                "# torque_conv_up_err, upper uncertainty on the convective torque\n"
                "# torque_conv_low_err, lower uncertainty on the convective torque\n"
                "# mean, mean of the Anderson-Darling test p-values\n"
                "# std, standard deviation of the Anderson-Darling test p-values\n")
    
    # add the top text to the top of the table in the zenodo folder
    with open(paths.data / "zenodo/Table_4_tidal_interaction.csv", "r") as f:
        lines = f.readlines()
    with open(paths.data / "zenodo/Table_4_tidal_interaction.csv", "w") as f:
        f.write(top_text)
        f.writelines(lines)


    # take absolute value of torque_conv_up_err and torque_conv_low_err
    # df.torque_conv_up_err = np.abs(df.torque_conv_up_err)
    # df.torque_conv_low_err = np.abs(df.torque_conv_low_err)

    # convert to latex readable entries 
    new_cols =  [r"$M_*$ [$M_\odot$]",
                r"$M_{\mathrm{p}} (\sin i)$ [$M_\oplus$]",
                r"log$_{10} 10^{-8} \Delta g / g$",
                r"log$_{10} \tau_{\rm tide}$ [yr]",
                r"$10^{-18} \frac{\partial L_{\rm conv}}{\partial t}$"
                r" $\left[M_\odot \left(\frac{km}{s}\right)^2\right]$",
                ]

    

    df["grav_pert"] = df["grav_pert"] * 1e8
    df["grav_pert_up_err"] = df["grav_pert_up_err"] * 1e8
    df["grav_pert_low_err"] = df["grav_pert_low_err"] * 1e8
    df["grav_pert_up_err"] = np.log10(df["grav_pert"] + df["grav_pert_up_err"]) - np.log10(df["grav_pert"])
    df["grav_pert_low_err"] = np.log10(df["grav_pert"] - df["grav_pert_low_err"]) - np.log10(df["grav_pert"])
    df["grav_pert"] = np.log10(df["grav_pert"])                                                        

    df["tidal_disip_timescale_up_err"] = np.log10(df["tidal_disip_timescale"] + df["tidal_disip_timescale_up_err"]) - np.log10(df["tidal_disip_timescale"])
    df["tidal_disip_timescale_low_err"] = np.log10(df["tidal_disip_timescale"] - df["tidal_disip_timescale_low_err"]) - np.log10(df["tidal_disip_timescale"])
    df["tidal_disip_timescale"] = np.log10(df["tidal_disip_timescale"])

    
    df["torque_conv"] = df["torque_conv"] * 1e18
    df["torque_conv_up_err"] = df["torque_conv_up_err"] * 1e18
    df["torque_conv_low_err"] = - df["torque_conv_low_err"] * 1e18

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
    df[r"ref. $M_{\rm p}$"] = df.pl_bmassj_bibkey.apply(lambda x: bibkeys[x])

    # add reference columns to new_cols
    new_cols.append(r"ref. $M_*$")
    new_cols.append(r"ref. $M_{\rm p}$")


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

