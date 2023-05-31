import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import paths


from adjustText import adjust_text

def get_sigma_values():
    """Define the sigma values."""

    # define sigma values
    onesigma = 0.3173
    twosigma = 0.0455
    threesigma = 0.0027
    
    # put them in a list
    sigmas = [onesigma, twosigma, threesigma]
    sigma_label = [r"$1\sigma$", r"$2\sigma$", r"$3\sigma$"]

    return sigmas, sigma_label

if __name__ == "__main__":


    # read the tidal interaction strength table with the AD test results
    res = pd.read_csv(paths.data / "TIS_with_ADtests.csv", index_col=0)


    # RV IDs
    rvs = ["Proxima Cen", "TAP 26", "GJ 3082", "GJ 3323", "GJ 687" , "YZ Cet", "GJ 674"]

    # add a column that is 1 for RV stars and 0 for others
    res["RV"] = [1 if ID in rvs else 0 for ID in res.ID.values]

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
    axes[0].set_ylabel("p-value of AD test", fontsize=13)

    # loop over the models
    for model, label in zip(models, labels):

        # pick an axis
        ax = axes.pop()
        
        # plot the data
        # torque conv is the model, use appropriate color, otherwise grey
        if model == "torque_conv":
            for color, h in res.groupby("color_conv"):
                
                # group by RV and non-RV
                for rv, g in h.groupby("RV"):

                    xerr = np.abs(np.asarray([g[model + "_low_err"], np.abs(g[model + "_up_err"])]))
                   
                    if rv == 1:
                        ax.errorbar(g[model],g["mean"], xerr=xerr,
                                    yerr=g["std"], label=color, 
                                color=color, fmt="X", markersize=7, elinewidth=0.3)
                    else:
                        ax.errorbar(g[model],g["mean"], xerr=xerr,
                                    yerr=g["std"], label=color, 
                                color=color, fmt="o", markersize=7, elinewidth=0.3)
                
          
        else:
            

            # group by RV and non-RV
            for rv, g in res.groupby("RV"):

                xerr = np.abs(np.asarray([g[model + "_low_err"], np.abs(g[model + "_up_err"])]))
                
                if rv == 1:
                    ax.errorbar(g[model],g["mean"], xerr=xerr,
                                yerr=g["std"], label=model, 
                            color="grey", fmt="X", markersize=7, elinewidth=0.3)
                else:
                    ax.errorbar(g[model],g["mean"], xerr=xerr,
                                yerr=g["std"], label=model, 
                            color="grey", fmt="o", markersize=7, elinewidth=0.3)

        

        # add the ID of the systems with low p-values
        texts = []
        _ = res[(res['mean']<.19) | (res["torque_conv"]>1e-15)]
        for i, row in _.iterrows():
            texts.append(ax.annotate(row["ID"], (row[model], row["mean"]), 
                                     fontsize=11,))
        # layout
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(label, fontsize=13)

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
