"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2023, MIT License

Script that grabs two light curves of planet hosts that we found with 
false positives, both physical (SSO) and instrumental (argabrightening),
makes a two panel figure for the appendix.
"""

import lightkurve as lk
import matplotlib.pyplot as plt

import paths


if __name__ == '__main__':


    # get Kepler light curve of Kepler-235
    kicname = 'Kepler-235'
    lcskic = lk.search_lightcurve('Kepler-235', author='Kepler', cadence='short', quarter=14)
    lckic = lcskic[2].download()
    kictitle = 'Instrumental False Positive: Possible Argabrightening'
    xlimkic = (1337.45, 1337.55)
    ylimkic = (5100, 5600)

    # get TESS light curve of TIC 435339847
    ticname = 'K2-77'
    lcstic = lk.search_lightcurve('TIC 435339847', cadence='short', sector=44)
    lctic = lcstic[0].download()
    tictitle = 'Physical False Positive: Solar System Object'
    xlimtic = (2516.6, 2518.3)
    ylimtic = (4500, None)

    # Get flare light curve of GJ 3323
    flcname = 'GJ 3323'
    lcs = lk.search_lightcurve('GJ 3323', author='SPOC', exptime=120, sector=5)
    flc = lcs[0].download()
    ftitle = 'Flare Light Curve'
    fxlim = (1445.5, 1445.9)
    fylim = (13200, 15800)

    # plot the light curves side by side in one figure
    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    flc.plot(ax=ax[0], linewidth=1, label=flcname)
    lckic.plot(ax=ax[1], linewidth=1, label=kicname)
    lctic.plot(ax=ax[2], linewidth=1, label=ticname)


    # set the limits of the x and y axes separately for each light curve
    ax[1].set_xlim(xlimkic)
    ax[1].set_ylim(ylimkic)
    ax[2].set_xlim(xlimtic)
    ax[2].set_ylim(ylimtic)
    ax[0].set_xlim(fxlim)
    ax[0].set_ylim(fylim)
    ax[0].set_title(ftitle)
    ax[1].set_title(kictitle)
    ax[2].set_title(tictitle)

    for a in ax:
        a.legend(frameon=False)

    plt.tight_layout()

    plt.savefig(paths.figures / 'systematics_false_positives.png', dpi=300)

