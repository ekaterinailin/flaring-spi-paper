import numpy as np

def trail(x, col, errcol, nalt): 
    n = x.log10err
    print(n)
    if np.isnan(n):
        return fr"${x[col]:.{nalt})f} [{x[errcol]:.0f}]$"
    elif n < 0:
        return fr"${x[col]:.0f} [{x[errcol]*10**(-n):.0f}]$"
    else:
        return fr"${x[col]:.{n}f} [{x[errcol]:.0f}]$"

def get_err_string(df,col,errcol, fillna=1, nalt=1):
    """Get the error string for a column with uncertainties"""
    
    df["log10err"] = np.floor(np.log10(df[errcol])) * (-1)
    df.log10err = df.log10err.fillna(fillna).astype(int) 

    df[col] = df.apply(lambda x: np.round(x[col], x.log10err), axis=1)
    df[errcol] = df.apply(lambda x: np.round(x[errcol] * 10**(x.log10err), 0), axis=1)


    return df.apply(lambda x: trail(x, col, errcol, nalt), axis=1)