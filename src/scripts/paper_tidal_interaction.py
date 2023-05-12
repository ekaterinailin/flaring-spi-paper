import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import paths


from adjustText import adjust_text

def get_sigma_values():
    """Define the sigma values."""

    # define sigma values
    onesigma = 1 - .342*2
    twosigma = 1 - .342*2 - .136*2
    threesigma = 1 - .342*2 - .136*2 - .021*2
    
    # put them in a list
    sigmas = [onesigma, twosigma, threesigma]
    sigma_label = [r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"]

    return sigmas, sigma_label


if __name__ == "__main__":


    # read the tidal interaction strength table with the AD test results
    res = pd.read_csv(paths.data / "TIS_with_ADtests.csv", index_col=0)

    # blue when convective envelope is spinning faster, and transferring angular momentum to the planet
    res["color_conv"] = ["blue" if np.sign(torque)==1 else "grey" for torque in res["torque_conv"].values]
    
    models = ["grav_pert", "tidal_disip_timescale", "torque_conv"]

    # convert all values and _err to absolute values
    for model in models:
        res[model] = np.abs(res[model])
        res[model + "_up_err"] = np.abs(res[model + "_up_err"])
        res[model + "_low_err"] = np.abs(res[model + "_low_err"])

    # initialize the figure
    fig, axes = plt.subplots(1,3, figsize=(15,5), sharey=True)
    axes = list(axes) 

    # define the models and labels
    
    labels = [r"gravitational perturbation $\Delta g / g$",
            r"tidal dissipation timescale $\tau_{\rm tide}$ [yr]",
            r"tidal torque $\partial L_{conv}/\partial t$ $\left[M_\odot \left(\frac{km}{s}\right)^2\right]$"]

    # define shared axis label
    axes[0].set_ylabel("p-value of AD test", fontsize=12)

    # loop over the models
    for model, label in zip(models, labels):

        # pick an axis
        ax = axes.pop()
        
        # plot the data
        # torque conv is the model, use appropriate color, otherwise grey
        if model == "torque_conv":
            for color, g in res.groupby("color_conv"):
                xerr = np.abs(np.asarray([g[model + "_low_err"], np.abs(g[model + "_up_err"])]))
                print(xerr)
                ax.errorbar(g[model],g["mean"], xerr=xerr,
                            yerr=g["std"], label=color, 
                        color=color, fmt="X", markersize=7, elinewidth=0.3)
          
        else:
            xerr = np.abs(np.asarray([res[model + "_low_err"], np.abs(res[model + "_up_err"])]))

            ax.errorbar(res[model],res["mean"], xerr=xerr,
                        yerr=res["std"], label=model, 
                       color="grey", fmt="X", markersize=7, elinewidth=0.3)

        # add the ID of the systems with low p-values
        texts = []
        _ = res[(res['mean']<.19) | (res["torque_conv"]>1e-15)]
        for i, row in _.iterrows():
            texts.append(ax.annotate(row["ID"], (row[model], row["mean"]), 
                                     fontsize=10,))
        # layout
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(label, fontsize=12)

        minx, maxx = res[model].min(), res[model].max()

        ax.set_xlim(minx*0.1, maxx*10)

        # add the sigma lines
        sigmas, sigma_label = get_sigma_values()
        for sigma, l in zip(sigmas, sigma_label):
            ax.axhline(sigma, color="k", linestyle="--", alpha=.5)
            ax.text(maxx*12, sigma, l, fontsize=10)

        # adjust label positions
        adjust_text(texts, ax=ax)

    # save to file
    plt.tight_layout()
    plt.savefig(paths.figures / "PAPER_tidal_AD_test.png", dpi=300)
