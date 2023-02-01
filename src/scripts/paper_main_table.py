"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that generates the main table of the paper, showing the
AD test results for the orbital period all stellar and planetary
parameters.
"""

import numpy as np
import pandas as pd
import paths

def citation_from_bibkey(bibkey):
    """Create a LaTeX citation from a bibkey.
    
    Parameters
    ----------
    bibkey : str
        The bibkey to use for the citation.
    
    Returns
    -------
    str
        The LaTeX citation.
    """
    return r" \citet{" + bibkey + "}"

def max_array(a, b):
    """Compute the maximum of two arrays. """
    a = a.astype(float)
    b = b.astype(float)
    return np.where(a > b, a, b)

def min_array(a, b):
    """Compute the minimum of two arrays. """
    a = a.astype(float)
    b = b.astype(float)
    return np.where(a < b, a, b)

def get_len_decimals(df, col, err, err2=None, typ="err"):
    """Get the number of decimals to round to.
    
    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data.
    col : str
        The column name of the value.
    err : str
        The column name of the error.
    err2 : str, optional    
        The column name of the second error.
    typ : str, optional
        The type of error. Can be "err" or "high-low".

    Returns
    -------
    int
        The number of decimals to round to.
    """
    if err2 is None:
        mr = max_array(np.abs(np.log10(np.abs(df[col])).astype(int).values)+2, 
                        np.abs(np.log10(np.abs(df[col] / df[err]))).astype(int).values + 2)

        return mr
    else:
    
        if typ=="err":
            minarr = min_array(df[err].values, -df[err2].values)
            mr = max_array(np.abs(np.log10(np.abs(df[col])).astype(int).values)+2, 
                         np.abs(np.log10(np.abs(df[col] / minarr)).astype(int).values) +2)
            return mr
        elif typ=="high-low":
            minarr = min_array((df[err]-df[col]).values, (df[col]-df[err]).values)
            
            mr =  max_array(np.abs(np.log10(np.abs(df[col])).astype(int).values)+2, 
                           np.abs(np.log10(np.abs(df[col] / minarr)).astype(int).values) + 2)
            return mr

def round_to_decimals(df, col, err, err2=None, typ="err"):

    """Round to the correct number of decimals.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data.
    col : str
        The column name of the value.
    err : str
        The column name of the error.
    err2 : str, optional    
        The column name of the second error.
    typ : str, optional
        The type of error. Can be "err" or "high-low".

    Returns
    -------
    pd.Series
        The rounded values.
    pd.Series
        The rounded errors.
    pd.Series
        The rounded second errors (optional).
    """

    df["_"] = get_len_decimals(df, col, err, err2=err2,typ=typ).astype(int)
    val = df.apply(lambda x: np.round(x[col], x._) if np.abs(x[err])<1 else  np.round(x[col],0).astype(int), axis=1)
    
    if err2 is None:
        err = df.apply(lambda x: np.round(x[err], x._) if x[err]<1 else np.round(x[err],0).astype(int), axis=1)
        del df["_"]
        return val, err
    else:
        if typ=="err":
            err = df.apply(lambda x: np.round(x[err], x._) if x[err]<1 else np.round(x[err],0).astype(int), axis=1)
            err2 = df.apply(lambda x: np.round(x[err2], x._) if x[err2]<1 else np.round(x[err],0).astype(int), axis=1)
        elif typ=="high-low":
            err = df.apply(lambda x: np.round(x[err] - x[col], x._) if x[err] - x[col]<1 else np.round(x[err]-x[col],0).astype(int), axis=1)
            err2 = df.apply(lambda x: np.round(x[err2] - x[col], x._) if x[col] - x[err2]<1 else np.round(x[err2] - x[col],0).astype(int), axis=1)
        del df["_"]
        return val, err, err2


def tex_up_low(val, err, err2):
    """Convert a value and two errors into a LaTeX string.

    Parameters
    ----------
    val : float
        The value.
    err : float
        The first error.
    err2 : float
        The second error.
    
    Returns
    -------
    str
        The LaTeX string.
    """

    return "$" + val.astype(str) + r"^{" + err.astype(str) + "}_{" + err2.astype(str) + "}$"

def tex_one_err(val, err):
    """Convert a value and one error into a LaTeX string.

    Parameters
    ----------
    val : float
        The value.
    err : float
        The error.

    Returns
    -------
    str
        The LaTeX string.
    """
    return val.astype(str) + "[" + err.astype(str) + "]"

# for each type of value cols, define a function that
# converts them into one list of strings for latex
def to_tex(df, col):
    """Convert a column into a LaTeX string.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data.
    col : list
        A list of column names.

    Returns
    -------
    pd.Series
        The LaTeX strings.
    """
    if len(col) == 4:
   
        if col[2][-6:] == "bibkey":

            val, err = round_to_decimals(df, col[0], col[1],typ=col[3])
            tex = tex_one_err(val, err) + citation_from_bibkey(df[col[2]])
   
        else:
   
            val, err, err2 = round_to_decimals(df, col[0], col[1], err2=col[2],typ=col[3])
            tex = tex_up_low(val, err, err2)
   
    elif len(col) == 5:
   
        val, err, err2 = round_to_decimals(df, col[0], col[1], err2=col[2],typ=col[4])
        tex = tex_up_low(val, err, err2) + citation_from_bibkey(df[col[3]])
   
    elif len(col) == 3:
   
        val, err = round_to_decimals(df, col[0], col[1], typ=col[2])
        tex = tex_one_err(val, err)
   
    else:
   
        tex = df[col[0]].astype(str)
   
    return tex

if __name__ == "__main__":


    # define the groups of strings that go together
    cols = [('st_rotp','st_rotp_err','st_rotp_bibkey', 'err'),
            ("orbper_d","orbper_d_err", "pl_orbper_bibkey", 'err'),
            ("st_rad","st_rad_err1", "st_rad_bibkey", 'err'),
            ("a_au","a_au_err","pl_orbsmax_bibkey",'err'),

            ('st_lum', 'st_lumerr1', 'st_lumerr2', 'st_lum_bibkey', 'err'),
            ("pl_radj",'pl_radjerr1', 'pl_radjerr2',"pl_radj_bibkey", 'err'),

            ("Ro","Ro_high","Ro_low", 'high-low'),
            ("B_G","B_G_high","B_G_low", 'high-low'),
            ("p_spi_erg_s","p_spi_erg_s_high","p_spi_erg_s_low",'high-low'),
            ('p_spi_kav22', 'p_spi_kav22_high','p_spi_kav22_low', 'high-low'),
            
            ("v_rel_km_s", 'v_rel_err_km_s', 'err'),

            ("mean", "std","err")]

    # define the latex column names
    map_col_names = {
        "st_rotp":"$P_{rot}$ [d]",
        "orbper_d":"$P_{orb}$ [d]",
        "st_rad":"$R_{*}$ [R$_\odot$]",
        "pl_radj":"$R_{p}$ [R$_J$]",
        "a_au":"$a$ [au]",
        "st_lum":"log${10} L_{*}$ [L$_\odot$]",
        "Ro":"Ro",
        "B_G":"$B$ [G]",
        "p_spi_erg_s":"log$_{10} P_{SPI,sb}$ [erg s$^{-1}$]",
        "p_spi_kav22":"log$_{10} P_{SPI,aw}$ [erg s$^{-1}$]",
        "v_rel_km_s":"$v_{rel}$ [km s$^{-1}$]",
        "mean":"p-value",
        }

    # read table to texify
    df = pd.read_csv(paths.data / "results.csv")


    # make log10 on following columns
    makelog = ["p_spi_erg_s","p_spi_erg_s_high","p_spi_erg_s_low",
            'p_spi_kav22', 'p_spi_kav22_high','p_spi_kav22_low']

    for col in makelog:
        df[col] = np.log10(df[col])

    # select only the columns we want
    sel = df[["ID","TIC",
                'st_rotp','st_rotp_err','st_rotp_source', 
                "orbper_d","orbper_d_err", "pl_orbper_bibkey",
                "multiple_star", "multiple_star_source",
                "st_rad","st_rad_err1", "st_rad_bibkey",
                "pl_radj",'pl_radjerr1', 'pl_radjerr2',"pl_radj_bibkey",
                "Ro","Ro_high","Ro_low",
                'st_lum', 'st_lumerr1', 'st_lumerr2', 'st_lum_bibkey', 
                "a_au","a_au_err","pl_orbsmax_bibkey",
                "B_G","B_G_high","B_G_low",
                "orbits_covered",
                "v_rel_km_s", 'v_rel_err_km_s',
                "p_spi_erg_s","p_spi_erg_s_high","p_spi_erg_s_low",
                'p_spi_kav22', 'p_spi_kav22_high','p_spi_kav22_low',
                "mean", "std"]]
    
    # select only the single stars
    singles = sel[sel.multiple_star.isnull()]

    # rename the column with the source of the rotation period
    singles = singles.rename(columns={"st_rotp_source":"st_rotp_bibkey"})

    # drop rows with TIC 67646988 and 236387002, the brown dwarfs
    singles = singles[singles.TIC != 67646988 ]
    singles = singles[singles.TIC != 236387002 ]

    fulltable = singles.copy()

    # convert the singles table to latex after converting the values to tex format
    print("Converting each parameter to a latex formatted column.")
    for col in cols:
        print(col)
        newname = map_col_names[col[0]]
        singles[newname] = to_tex(singles, col)
        for c in col:
            if (c in singles.columns) & (newname != c):
                del singles[c]

    # delete some columns that are not needed
    del singles["multiple_star"]
    del singles["multiple_star_source"]
    del singles["orbits_covered"]

    # make TeX table
    # print("Converting table to TeX format.")

    # # make the default string length longer
    # pd.set_option('display.max_colwidth', 1000)

    # string = singles.to_latex(escape=False,index=False)

    # # layout
    # string = string.replace("\citet{[*]}","[*]")
    # string = string.replace("midrule","hline")
    # string = string.replace("toprule","hline")
    # string = string.replace("bottomrule","hline")

    # # write to file
    # path = paths.output / "fit_parameters.tex"
    # print("Write to file: ", path)

    # with open(path, "w") as f:
    #     f.write(string)


    # Get all bibkeys from singles table
    bibkeys = fulltable.st_rotp_bibkey.unique()
    bibkeys = np.append(bibkeys, fulltable.pl_orbper_bibkey.unique())
    bibkeys = np.append(bibkeys, fulltable.st_rad_bibkey.unique())
    bibkeys = np.append(bibkeys, fulltable.pl_radj_bibkey.unique())
    bibkeys = np.append(bibkeys, fulltable.pl_orbsmax_bibkey.unique())
    bibkeys = np.append(bibkeys, fulltable.st_lum_bibkey.unique())

    # enumerate the bibkeys
    bibkeys = np.unique(bibkeys)

    # make a dictionary with the bibkeys and the corresponding index
    bibkeys = {bibkeys[i]:i+1 for i in range(len(bibkeys))}

    # # replace the bibkeys with the index in the string table
    # for key in bibkeys.keys():
    #     replace = "\citet{"+key+"}"
    #     string = string.replace(replace, "(" + str(bibkeys[key]) + ")")

    # # write to file
    # path = paths.output / "fit_parameters_bibkeys.tex"
    # print("Write to file: ", path)

    # with open(path, "w") as f:
    #     f.write(string)


    # literature parameters table columns
    lit_cols = ["ID", "TIC", "$P_{rot}$ [d]", "$P_{orb}$ [d]", "$R_{*}$ [R$_\odot$]",
            "$R_{p}$ [R$_J$]", "$a$ [au]", "log${10} L_{*}$ [L$_\odot$]"]

    # derived parameters table columns
    der_cols = ["ID", "Ro", "$B$ [G]", "log$_{10} P_{SPI,sb}$ [erg s$^{-1}$]",
                "log$_{10} P_{SPI,aw}$ [erg s$^{-1}$]", "$v_{rel}$ [km s$^{-1}$]",
                "p-value",]

    # make a list of tuples with the two column lists
    splitcols = [("lit", lit_cols), ("der", der_cols)]

    # SPLIT TABLE IN TWO

    for label, cs in splitcols:

        # make a new singles table with the literature parameters
        lit_singles = singles[cs]

        # make TeX table
        print("Converting table to TeX format.")

        # make the default string length longer
        pd.set_option('display.max_colwidth', 1000)

        # convert to LaTeX
        string = lit_singles.to_latex(escape=False,index=False)

        # layout
        string = string.replace("\citet{[*]}","[*]")
        string = string.replace("midrule","hline")
        string = string.replace("toprule","hline")
        string = string.replace("bottomrule","hline")

        # replace the bibkeys with the index in the string table
        for key in bibkeys.keys():
            replace = "\citet{"+key+"}"
            string = string.replace(replace, "(" + str(bibkeys[key]) + ")")

        # write to file
        path = paths.output / f"table_{label}_vals.tex"
        print("Write to file: ", path)

        with open(path, "w") as f:
            f.write(string)

            