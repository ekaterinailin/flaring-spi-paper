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

import paths

import adjustText as aT

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

    # adjust text positions
    aT.adjust_text(txts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5),
                   ax=ax1)

    # ---------------------------------------------------------------------
    # Lower panel: Lx vs B

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

    # adjust text positions
    aT.adjust_text(txts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5),
                   ax=ax2)


    # save
    plt.tight_layout()
    plt.savefig(paths.figures / 'PAPER_lxlbol.png', dpi=300)