"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that generates the main tables of the paper, showing 1. all stellar and 
planetary parameters necessary for analysis (and producing a string of 
references for the footnote), and 2. derived parameters and AD test results 
for the orbital period. 
"""

import numpy as np
import pandas as pd
import paths
import re



def round_to_1(x):
    if x == 0:
        return 0
    elif np.isnan(x):
        return np.nan
    else:
        return np.round(x, -int(np.floor(np.log10(np.abs(x)))))
    

def g(row, oneerr=False):
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
        if oneerr:
            try:
                v = np.min([np.abs(row[col[0]]),np.abs(row[col[1]])])
                n  = -int(np.floor(np.log10(np.abs(v))))
            except:
                n = 1
        else:
            
            try:
                v = np.min([row[col[1]],row[col[2]]])
                n  = -int(np.floor(np.log10(np.abs(v))))
            
            except:

                n = 1
     
        if n < 0:
            if oneerr:
                return f"${int(np.round(row[col[0]], n)):d} [{int(np.round(row[col[1]], n)):d}]$"

            else:
               return (f"${np.round(row[col[0]], n):d}" +
                        r"^{" +
                        f"{np.round(row[col[1]], n):d}" +
                        r"}_{" +
                        f"{np.round(row[col[2]], n):d}" +
                        r"}$")
        else:
            if oneerr:
                v1 = np.round(row[col[0]], n)
                v2 = np.round(row[col[1]], n)
                return f"${v1:.{n}f} [{v2:.{n}f}]$"
            else:
                return (f"${row[col[0]]:.{n}f}" + 
                        r"^{" + 
                        f"{row[col[1]]:.{n}f}" + 
                        r"}_{" + 
                        f" {row[col[2]]:.{n}f}" + 
                        r"}$") 
    



if __name__ == "__main__":


    # define the groups of strings that go together
    cols = [('st_rotp','st_rotp_err','st_rotp_bibkey', 'err'),
            ("orbper_d","orbper_d_err", "pl_orbper_bibkey", 'err'),
            ("st_rad","st_rad_err1", "st_rad_bibkey", 'err'),
            ("a_au","a_au_err","pl_orbsmax_bibkey",'err'),

            ('st_lum', 'st_lumerr1', 'st_lumerr2', 'st_lum_bibkey', 'aerr'),
            ("pl_radj",'pl_radjerr1', 'pl_radjerr2',"pl_radj_bibkey", 'aerr'),
            ("pl_orbeccen", "pl_orbeccenerr1", "pl_orbeccenerr2", "pl_orbeccen_bibkey", 'aerr'),

            ("Ro","Ro_high","Ro_low", 'high-low'),
            ("B_G","B_G_high","B_G_low", 'high-low'),
            ("p_spi_sb_bp1_erg_s","p_spi_sb_bp1_erg_s_high","p_spi_sb_bp1_erg_s_low",'high-low'),
            ('p_spi_aw_bp1_erg_s', 'p_spi_aw_bp1_erg_s_high','p_spi_aw_bp1_erg_s_low', 'high-low'),
            ("p_spi_sb_bp0_erg_s","p_spi_sb_bp0_erg_s_high","p_spi_sb_bp0_erg_s_low",'high-low'),
            ('p_spi_aw_bp0_erg_s', 'p_spi_aw_bp0_erg_s_high','p_spi_aw_bp0_erg_s_low', 'high-low'),
            
            ("v_rel_km_s", 'v_rel_err_km_s', 'err'),

            ("mean", "std","err")]
    
    # define the latex column names
    map_col_names = {
        "st_rotp":r"$P_{\rm rot}$",
        "orbper_d":r"$P_{\rm orb}$",
        "st_rad":r"$R_{*}$",
        "pl_radj":r"$R_{\rm p}$",
        "a_au":r"$a$",
        "pl_orbeccen":"$e$",
        "st_lum":"log$_{10} L_{*}$",
        "Ro":r"$R$o",
        "B_G":r"$B$",
        "p_spi_sb_bp1_erg_s":r"log$_{10} P_{\rm spi,sb}$",
        "p_spi_aw_bp1_erg_s":r"log$_{10} P_{\rm spi,aw}$",
        "p_spi_sb_bp0_erg_s":r"log$_{10} P_{\rm spi,sb0}$",
        "p_spi_aw_bp0_erg_s":r"log$_{10} P_{\rm spi,aw0}$",
        "v_rel_km_s":r"$v_{\mathrm{rel}}$",
        "mean":r"$p$-value",
        "obstime_d":"obs. time",
        }
    


    # read table to texify
    df = pd.read_csv(paths.data / "results.csv")

    # convert au and au_err to 10^-2 au
    df["a_au"] = df["a_au"] * 100
    df["a_au_err"] = df["a_au_err"] * 100

    # select only the columns we want
    sel = df[["ID","TIC",'obstime_d',
                'st_rotp','st_rotp_err','st_rotp_source', 
                "orbper_d","orbper_d_err", "pl_orbper_bibkey",
                "pl_orbeccen", "pl_orbeccenerr1", "pl_orbeccenerr2", "pl_orbeccen_bibkey",
                "multiple_star", "multiple_star_source",
                "st_rad","st_rad_err1", "st_rad_bibkey",
                "pl_radj",'pl_radjerr1', 'pl_radjerr2',"pl_radj_bibkey",
                "Ro","Ro_high","Ro_low",
                'st_lum', 'st_lumerr1', 'st_lumerr2', 'st_lum_bibkey', 
                "a_au","a_au_err","pl_orbsmax_bibkey",
                "B_G","B_G_high","B_G_low",
                "orbits_covered",
                "v_rel_km_s", 'v_rel_err_km_s',
                "p_spi_sb_bp1_erg_s","p_spi_sb_bp1_erg_s_high","p_spi_sb_bp1_erg_s_low",
               'p_spi_aw_bp1_erg_s', 'p_spi_aw_bp1_erg_s_high','p_spi_aw_bp1_erg_s_low', 
               "p_spi_sb_bp0_erg_s","p_spi_sb_bp0_erg_s_high","p_spi_sb_bp0_erg_s_low",
               'p_spi_aw_bp0_erg_s', 'p_spi_aw_bp0_erg_s_high','p_spi_aw_bp0_erg_s_low',
                "mean", "std",]]
    

    
    # select only the single stars
    singles = sel[sel.multiple_star.isnull()]



    # drop rows with TIC 67646988 and 236387002, the brown dwarfs
    singles = singles[singles.TIC != "67646988" ]
    singles = singles[singles.TIC != "236387002" ]

    # the old Kepler-411 instance
    singles = singles[singles.TIC != "399954349(c)" ]

    # GJ 1061 because rotation is unclear
    singles = singles[singles.TIC != "79611981" ]


    # rename the column with the source of the rotation period
    singles = singles.rename(index=str, columns={"st_rotp_source":"st_rotp_bibkey",
                                                  "obstime_d":"obs. time"})


    # sort table by p-value
    singles = singles.sort_values(by="mean", ascending=False)

    fulltable = singles.copy()


    # calc log10 of the values in the list of columns
    convtolog10 = ["p_spi_sb_bp1_erg_s","p_spi_sb_bp1_erg_s_high","p_spi_sb_bp1_erg_s_low",
                    'p_spi_aw_bp1_erg_s', 'p_spi_aw_bp1_erg_s_high','p_spi_aw_bp1_erg_s_low', 
                    "p_spi_sb_bp0_erg_s","p_spi_sb_bp0_erg_s_high","p_spi_sb_bp0_erg_s_low",
                    'p_spi_aw_bp0_erg_s', 'p_spi_aw_bp0_erg_s_high','p_spi_aw_bp0_erg_s_low']
            
    for col in convtolog10:
        singles[col] = np.log10(singles[col])


    # round B_G and errors to int
    singles["B_G"] = (singles["B_G"].round(0).values).astype(int)
    singles["B_G_high"] = (singles["B_G_high"].round(0).values).astype(int)
    singles["B_G_low"] = (singles["B_G_low"].round(0).values).astype(int)

    # round obs. time to 1 decimal
    singles["obs. time"] = singles.apply(lambda x: f"{x['obs. time']:.1f}", axis=1)


    # convert the singles table to latex after converting the values to tex format
    print("Converting each parameter to a latex formatted column.")


    for col in cols:
        newname = map_col_names[col[0]]

        if col[-1] == "aerr":

            singles[newname] = singles.apply(g, axis=1)

        elif col[-1] == "err":

            g1 = lambda row: g(row, oneerr=True)
            singles[newname] = singles.apply(g1, axis=1)

        elif col[-1] == "high-low":

            singles[col[1]] = singles[col[1]] - singles[col[0]]
            singles[col[2]] = singles[col[2]] - singles[col[0]] 

            singles[newname] = singles.apply(g, axis=1)

        if "bibkey" in col[-2]:
            singles[newname] = singles.apply(lambda x: str(x[newname]) + " \citet{" + str(x[col[-2]]) + "}", axis=1)
 
        for c in col:
            if (c in singles.columns) & (newname != c):
                del singles[c]

    # delete some columns that are not needed
    del singles["multiple_star"]
    del singles["multiple_star_source"]
    del singles["orbits_covered"]

    

    # Get all bibkeys from singles table
    bibkeys = fulltable.st_rotp_bibkey.dropna().unique()
    bibkeys = np.append(bibkeys, fulltable.pl_orbper_bibkey.dropna().unique())
    bibkeys = np.append(bibkeys, fulltable.st_rad_bibkey.dropna().unique())
    bibkeys = np.append(bibkeys, fulltable.pl_radj_bibkey.dropna().unique())
    bibkeys = np.append(bibkeys, fulltable.pl_orbsmax_bibkey.dropna().unique())
    bibkeys = np.append(bibkeys, fulltable.st_lum_bibkey.dropna().unique())
    bibkeys = np.append(bibkeys, fulltable.pl_orbeccen_bibkey.dropna().unique())

    # enumerate the bibkeys
    bibkeys = np.unique(bibkeys)

    # make a dictionary with the bibkeys and the corresponding index
    bibkeys = {bibkeys[i]:i+1 for i in range(len(bibkeys))}

    # literature parameters table columns
    lit_cols = ["ID", r"$P_{\rm rot}$", r"$P_{\rm orb}$", "$R_{*}$",
            r"$R_{\rm p}$", "$a$", "$e$", "log$_{10} L_{*}$", "obs. time"]

    # derived parameters table columns
    der_cols = ["ID", r"$R$o", r"$B$", r"$v_{\mathrm{rel}}$", 
                r"log$_{10} P_{\rm spi,sb}$",
                r"log$_{10} P_{\rm spi,sb0}$", 
                r"log$_{10} P_{\rm spi,aw}$", 
                r"log$_{10} P_{\rm spi,aw0}$", r"$p$-value",]
    
    lit_unit_row = ['', '[d]', '[d]', r'[R$_\odot$]', r'[R$_J$]', r'[$10^{-2}$ au]',
                     '', r'[L$_\odot$]', "[d]"]
    der_unit_row = ['', '', '[G]', r'[km s$^{-1}$]', r'[erg s$^{-1}$]', r'[erg s$^{-1}$]', 
                    r'[erg s$^{-1}$]', r'[erg s$^{-1}$]',  '']

    # make a list of tuples with the two column lists
    splitcols = [("lit", lit_cols, lit_unit_row), ("der", der_cols, der_unit_row)]


    # SPLIT TABLE IN TWO

    for label, cs, unit_row in splitcols:

        # make a new singles table with the literature parameters
        lit_singles = singles[cs]

        # insert unit row as first row
        lit_singles = lit_singles.reset_index(drop=True) # reset first
        
        lit_singles.loc[-1] = unit_row # then add line
        lit_singles.index = lit_singles.index + 1 # up index
        lit_singles = lit_singles.sort_index() # sort

        # make TeX table
        print("Converting table to TeX format.")

        # make the default string length longer
        pd.set_option('display.max_colwidth', 1000)

        # convert to LaTeX
        string = lit_singles.to_latex(escape=False,index=False)

        # layout
        string = string.replace(r"$nan^{nan}_{nan}$",r"--")
        string = string.replace(r"nan",r"-")
        string = string.replace(r"NaN",r"-") 
        string = string.replace(r"$-^{-}_{ -}$",r"-")
        string = string.replace("0.0e+00",r"0.0")
        string = string.replace("\citet{-}",r"")
        string = string.replace("\midrule","")
        string = string.replace("toprule","hline")
        string = string.replace("bottomrule","hline")
        try:
            string = string.replace(r"[L$_\odot$] \\",r"[L$_\odot$] \\ \hline")
        except:
            continue
        try:
            string = string.replace(r"[erg s$^{-1}$] &  \\",r"[erg s$^{-1}$] &  \\ \hline")
        except:
            continue

        if label == "lit":
            note = (r"We note that we found K2-354 under EPIC 211314705 and K2-329(!)"
                    r" in \citet{bouma2020cluster}, who refer to the detection paper"
                    r" \citep{pope2016transiting}, and also under TIC 468989066.")
            
            string = string.replace(r"K2-354",r"K2-354\footnote{" + note + "}")

        for n in range(1,10):
            string = string.replace(fr"e-0{n}",fr"\text{{e-}}{n}")

        # replace the bibkeys with the index in the string table
        for key in bibkeys.keys():
            replace = "\citet{"+key+"}"
            string = string.replace(replace, "(" + str(bibkeys[key]) + ")")

        # substitute "--" with any " (*)"" behind it with just "-" using regex
        string = re.sub(r"-- \(.+?\)", "-", string)

        # write to file
        path = paths.output / f"table_{label}_vals.tex"
        print("Write to file: ", path)

        with open(path, "w") as f:
            f.write(string)

    # generate a bibkey string to put in the footnote of the tex table
    bibstring = ""
    for key in bibkeys.keys():
        bibstring += "(" + str(bibkeys[key]) + ") \citet{" + key + "}, "
    
    bibstring = bibstring[:-2] + "."
   
    # write the bibstring to a file
    path = paths.output / "lit_table_bibstring.tex"
    print("Write footnote list to file: ", path)

    with open(path, "w") as f:
        f.write(bibstring)

            