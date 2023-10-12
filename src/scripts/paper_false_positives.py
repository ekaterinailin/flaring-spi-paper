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
    lcskic = lk.search_lightcurve('Kepler-235', author='Kepler', cadence='short', quarter=14)
    lckic = lcskic[2].download()
    kictitle = 'Instrumental False Positive: Possible Argabrightening'
    xlimkic = (1337.45, 1337.55)
    ylimkic = (5100, 5600)

    # get TESS light curve of TIC 435339847
    lcstic = lk.search_lightcurve('TIC 435339847', cadence='short', sector=44)
    lctic = lcstic[0].download()
    tictitle = 'Physical False Positive: Solar System Object'
    xlimtic = (2516.6, 2518.3)
    ylimtic = (None, None)

    # plot the light curves side by side in one figure
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    lckic.plot(ax=ax[0], linewidth=1)
    lctic.plot(ax=ax[1], linewidth=1)

    # set the limits of the x and y axes separately for each light curve
    ax[0].set_xlim(xlimkic)
    ax[0].set_ylim(ylimkic)
    ax[1].set_xlim(xlimtic)
    ax[1].set_ylim(ylimtic)
    ax[0].set_title(kictitle)
    ax[1].set_title(tictitle)

    for a in ax:
        a.legend(frameon=False)

    plt.tight_layout()

    plt.savefig(paths.figures / 'systematics_false_positives.png', dpi=300)

