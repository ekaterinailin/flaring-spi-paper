rule flares:
    output:
        "src/data/PAPER_flare_table.csv"
    cache:
        True
    script:
        "src/scripts/paper_latex_flare_table.py"
