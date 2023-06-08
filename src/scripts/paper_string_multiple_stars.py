"""
Python 3.8 -- UTF-8

Ekaterina Ilin, 2022, MIT License

Script that generates a list of excluded stars based on multiplicity and
contamination, with reference to where the multiplicity info was found.
"""

import pandas as pd

import paths

if __name__ == "__main__":

    # read table
    print("[UP ]Read results table ", paths.data / "results.csv")
    df = pd.read_csv(paths.data / "results.csv")

    # select only multiple or contaminated stars
    multiples = df[~df.multiple_star.isnull()]

    # make a string of IDs with multiple_star_source attached in \cite{}
    multiples["multiple_star_source"] = multiples.multiple_star_source.apply(lambda x: f"~\\citep{{{x}}}")

    # append the multiple_star_source to the ID and give one comma separated big string
    multiples = multiples.ID + multiples.multiple_star_source
    multiples = ", ".join(multiples)

    multiples = multiples + "."

    # write to file
    print("Write to file ", paths.output / "multiples_string.tex")
    with open(paths.output / "multiples_string.tex", "w") as f:
        f.write(multiples)