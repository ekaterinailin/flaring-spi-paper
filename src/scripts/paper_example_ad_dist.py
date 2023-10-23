
import lightkurve as lk
import numpy as np
import matplotlib.pyplot as plt 
import emcee
from scipy.stats import scoreatpercentile
from scipy.interpolate import interp1d
from scipy.misc import derivative
import paths


def sample_AD_for_custom_distribution(f, nobs, N):
    """
    
    Parameters:
    ------------
    f : func
        expected cum. dist. function (EDF)
    nobs : int
        size of data sample
    N : int
        number of samples to draw from the expected 
        distribution of flare phases

    Returns:
    ---------
    A2 : N-array
    """

   
    def func(x):
        if (x >= 1) | (x <= 0):
            return -np.inf
        else:
            lp =  np.log(derivative(f, x, dx=np.min([1e-4, (1-x)/3, x/3])))
            if np.isnan(lp):
                return -np.inf
            else:
                
                return lp[0]
        

    # Apply ensemble sampler from emcee
    
    # Sample from a 1-D distribution
    # Sample nobs values from the distribution
    # because the distrbution of the AD statistic
    # crucially depends on the sample size
    ndim, nwalkers = 1, nobs
    
    # initial state of the sampler is random values between 0 and 1
    p0 = np.random.rand(nwalkers, ndim)
    
    # Define the sampler with func as the distribution to sample from
    sampler = emcee.EnsembleSampler(nwalkers, ndim, func)
    
    # Run MCMC for N steps
    sampler.run_mcmc(p0, N, progress=True)
    
    # Get the samples
    samples = sampler.get_chain()

    # replace infs
    missing = np.where(~np.isfinite(samples))[0]
    if len(missing) > 0:
        samples[missing] = f(np.random.rand(*missing.shape))
    c = samples.reshape((N,nobs))
 
    # calculate the AD statistic for all samples
    A2 = np.array([anderson_custom(c[i,:], f) for i in range(N)])
    
    # make sure that converting shapes and calculating the statistic
    # preserved the number of samples correctly
    assert len(A2) == N
    
    return A2



def anderson_custom(x, dist):
    """
    Anderson-Darling test for data coming from a particular distribution
    The Anderson-Darling test is a modification of the Kolmogorov-
    Smirnov test `kstest` for the null hypothesis that a sample is
    drawn from a population that follows a particular distribution.
    For the Anderson-Darling test, the critical values depend on
    which distribution is being tested against.  
    Parameters
    ----------
    x : array_like
        array of sample data
    dist : func
        epected cum. distribution func (EDF)
    Returns
    -------
    A2 : float
        The Anderson-Darling test statistic
    """

    y = np.sort(x)
    z = dist(y)

    # A2 statistic is undefined for 1 and 0
    z = z[(z<1.) & (z>0.)]
  
    N = len(z)
    i = np.arange(1, N + 1)
    S = np.sum((2 * i - 1.0) / N * (np.log(z) + np.log(1 - z[::-1])), axis=0)
    A2 = - N - S

    return A2


def get_null_hypothesis_distribution(p, cum_n_exp):
    """Calculate the null hypothesis distribution.
    
    Parameters:
    -----------
    p : array
        array of phases for the flares
    cum_n_exp : array
        cumulative distribution of the observed phases
    
    Returns:
    --------
    null_hypothesis : scipy.interpolate.interpolate.interp1d
        interpolation function for the null hypothesis distribution
    """
    # add the (0,0) and (1,1) points to the cdf
    cphases = np.insert(p, 0, 0)
    cphases = np.append(cphases, 1.)

    # Interpolate!
    return interp1d(cphases, cum_n_exp, fill_value="extrapolate")

if __name__ == "__main__":

    # download HIP 67522 TESS lcs
    lcs = lk.search_lightcurve('HIP 67522', mission='TESS', cadence="short", author="SPOC").download_all()#.stitch().remove_nans()

    # from all lcs, extract the time and convert to orbital phase with period 6.95 d
    times = []
    for lc in lcs:
        times.append(lc.time.value)
    times = np.concatenate(times)
    times = (times % 6.95) / 6.95
    # assume for simplicity that the flare rate is constant
    # calculate the expected distribution function with the time array
    # and the flare rate

    # produce an array of 12 orbital phases from paper
    flares_ = np.array([0.61256542337174,
                        0.029301729581047,
                        0.017527257576216,
                        0.811732598451724,
                        0.057241154463297,
                        0.729890495361688,
                        0.040306751646131,
                        0.113071753157355,
                        0.150647085333129,
                        0.200293264178819,
                        0.948623252939387,
                        0.044963590199154])
    
    # sort the array
    flares_ = np.sort(flares_)


    # add zero to the beginning and one to the end
    flares = np.concatenate([[0], flares_, [1]])

    # make histogram
    hist = np.histogram(times, bins=flares)[0]

    # make cumulative histogram
    cum_hist = np.cumsum(hist)

    # normalize
    cum_hist = cum_hist / cum_hist[-1]

    # add zero to the beginning
    cum_hist_ = np.concatenate([[0], cum_hist])


    plt.plot(flares, cum_hist_)
    # plt.xlim(0, 1)

    print(cum_hist_.shape, flares_.shape)
    # make an EDF from the cum_hist
    f = get_null_hypothesis_distribution(flares_,cum_hist_)
    # sample AD from the distribution
    ad = sample_AD_for_custom_distribution(f, len(flares_), 10000)

    # percentile of the AD distribution the statistic falls into
    # but two-sided
    ad_ = np.copy(ad)

    med = np.mean(ad)
    below_med = (ad < med)
    ad[below_med] = med + (med - ad[below_med])


    plt.figure(figsize=(6,5))
    for perc, ls, sig in zip([68.27, 95.45, 99.75],[":", "--", "-."],[1,2,3]):

        adval = scoreatpercentile(ad, perc)

        plt.axvline(adval, label=fr"$p={((100-perc)/100):.3f}\;({sig}\sigma)$", linestyle=ls, color="k")


    plt.axvline(4.5, label="HIP 67522, $p=0.0056$", linestyle="-", color="r")

    plt.hist(ad_, bins=100)
    plt.xlim(0, adval+8)
    plt.legend(loc=1, fontsize=12, frameon=False)
    plt.xlabel(r"$A^2$ statistic", fontsize=13)
    plt.ylabel("Number of samples", fontsize=13)
    plt.tight_layout()

    plt.savefig(paths.figures / "example_ad_dist.png", dpi=300)
    