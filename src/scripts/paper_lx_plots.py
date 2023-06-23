"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2023, MIT License

Script that generates the figures that compare the X-ray luminosity of the
sources in the sample to the Rossby number and magnetic field strength.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from astropy.constants import L_sun
from astropy.table import Table

import paths

import adjustText as aT


def tau_wright2018(V, Ks, err=False, eV=None, eKs=None):
    """Convective turnover time from Wright et al. 2018 using
    Eq. 5 from that paper.

    Parameters
    ----------
    V : float
        The V magnitude of the star.
    Ks : float
        The Ks magnitude of the star.
    err : bool, optional
        If True, return the error on the Rossby number.
        The default is False.
    eV : float, optional
        The error on the V magnitude of the star.
        The default is None.
    eKs : float, optional
        The error on the Ks magnitude of the star.
        The default is None.

    Returns 
    -------
    tau : float
        The convective turnover time of the star.
    tau_err_high : float
        The upper error on the convective turnover time.
    tau_err_low : float
        The lower error on the convective turnover time.

    """

    tau = 0.64 + 0.25 * (V - Ks)

    if err:
        tau_err_high = 0.74 + 0.33 * (V + eV - Ks + eKs)
        tau_err_low = 0.54 + 0.17 * (V - eV - Ks - eKs)
        return 10**tau, 10**tau_err_high, 10**tau_err_low
    else:
        return 10**tau



if __name__ == "__main__":

    # convert L_sun to erg/s
    L_sun = L_sun.to('erg/s').value

    # read in the data
    df = pd.read_csv(paths.data / 'results.csv')

    # calculate Lx/Lbol
    lxlbol = df.xray_flux_erg_s/10**df.st_lum/L_sun

    # error propagation
    lxlbol_err = lxlbol * np.sqrt((df.xray_flux_err_erg_s/df.xray_flux_erg_s)**2 +
                                  ((df.st_lumerr1-df.st_lumerr2)/2./df.st_lum)**2)
    
    # make the plot
    fig, [ax1, ax2] = plt.subplots(ncols=1, nrows=2, figsize=(6,9))


    # ---------------------------------------------------------------------
    # Upper panel: Lx vs Ro


    # read Wright et al. 2011 data
    wright2011 = Table.read(paths.data / "wright2011.fit")
    wright2011["tau"] = tau_wright2018(wright2011["Vmag"], wright2011["Vmag"] - wright2011["V-K"])
    wright2011["Ro"] = wright2011["Prot"] / wright2011["tau"]   

        
    # Wright et al. 2011 data
    ax1.scatter(wright2011["Ro"].value, 10**wright2011["Lx_bol"].value,
                label="Wright et al. 2011", c="grey", zorder=-10, marker="x", alpha=0.2)

    ax1.errorbar(df.Ro, lxlbol, xerr=[df.Ro - df.Ro_low, df.Ro_high - df.Ro],
                yerr=lxlbol_err, markersize=8, fmt="d")
    
    # annotate with ID
    txts = []
    for i, row in df.iterrows():
        txt = ax1.annotate(row.ID, (row.Ro, lxlbol[i]), fontsize=11)
        txts.append(txt)

    # layout
    ax1.set_xlabel('Rossby number', fontsize=14)
    ax1.set_ylabel(r'$L_X/L_{bol}$', fontsize=14)
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # add legend
    ax1.legend(loc='lower left', fontsize=13, frameon=True)

    # adjust text positions
    aT.adjust_text(txts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5),
                   ax=ax1)

    # ---------------------------------------------------------------------
    # Lower panel: Lx vs B

    # read Reiners et al. 2022 data tsv with tab delimiter
    reiners2022 = pd.read_csv(paths.data / "reiners2022.tsv", delimiter="\t",
                              skiprows=72)
    # replace empty strings
    reiners2022.replace('     ', np.nan, inplace=True)

    # plot Reiners et al. 2022 data as scatter
    ax2.scatter(reiners2022["<B>"].astype(float),
                10**reiners2022["logLX/Lbol"].astype(float), 
                label="Reiners et al. 2022",
                c="grey", zorder=-10, marker="x", alpha=0.55)

    ax2.errorbar(df.B_G, lxlbol, markersize=8, 
                xerr=[df.B_G - df.B_G_low, df.B_G_high - df.B_G],
                yerr=lxlbol_err, fmt='d')

    # annotate with ID
    txts = []
    for i, row in df.iterrows():
        txt = ax2.annotate(row.ID, (row.B_G, lxlbol[i]), fontsize=11)
        txts.append(txt)
        
    ax2.set_xlabel('B [G]', fontsize=14)
    ax2.set_ylabel(r'$L_X/L_{bol}$', fontsize=14)
    ax2.set_xscale('log')
    ax2.set_yscale('log')

    # add legend
    ax2.legend(loc='lower right', fontsize=13, frameon=True)

    # adjust text positions
    aT.adjust_text(txts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5),
                   ax=ax2)


    # save
    plt.tight_layout()
    plt.savefig(paths.figures / 'PAPER_lxlbol.png', dpi=300)