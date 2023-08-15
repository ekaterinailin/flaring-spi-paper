"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that generates a table showing the powers for AU Mic interaction, to which
the results in the paper are normalized.
"""

import pandas as pd
import paths
import numpy as np


if __name__ == "__main__":

    # read results
    df = pd.read_csv(paths.data / "results.csv")

    # select AU Mic
    aumicspi = df.loc[df.TIC == "441420236"]

    # select SPI scenarios
    vals = [("p_spi_erg_s", r"P_{\rm spi,sb}$", "stretch-and-break, magnetized planet"),
            ("p_spi_erg_s_bp0", r"P_{\rm spi,sb0}$", "stretch-and-break, unmagnetized planet"),
            ("p_spi_kav22", r"P_{\rm spi,aw}$", r"Alfv\'en wing, magnetized planet"),
            ("p_spi_kav22_bp0", r"P_{\rm spi,aw0}$", r"Alfv\'en wing, unmagnetized planet")]

    # init SPI tab
    aumictab = pd.DataFrame(columns=["SPI scenario","abbrev.","AU Mic power [erg/s]"])

    # convert to latex vals and add to tab
    for val, symb, expl in vals:
        v = aumicspi[val].values[0]
        up = aumicspi[val + "_high"].values[0]
        low = aumicspi[val + "_low"].values[0]
        log10 = np.log10(v).round(0)
        uperr = (up-v) / 10**log10
        lowerr = (low-v) / 10**log10
        v = v / 10**log10
        valstr = fr"${v:.1f}" + r"^{" + fr"{uperr:.1f}" + r"}_{" + fr"{lowerr:.1f}" + r"} \times 10" +r"^{" + f"{log10:.0f}" +"}$"
        # print(symb, expl, valstr)
        aumictab = pd.concat([aumictab, pd.DataFrame({"SPI scenario": [expl], "abbrev.": [symb], "AU Mic power [erg/s]": [valstr]})], ignore_index=True)

    # convert to latex
    string = aumictab.to_latex(index=False, escape=False)
    string = string.replace("lll", "lcr")
    string = string.replace(r"\midrule", r"\hline")
    string = string.replace(r"\toprule", "")
    string = string.replace(r"\bottomrule", r"\hline")

    # write to file
    path = paths.output / "aumic_spi.tex"

    with open(path, "w") as f:
        f.write(string)
