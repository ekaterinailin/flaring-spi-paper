rule flares:
    input:
        "src/data/PAPER_flare_table.csv"
    output:
        "src/tex/output/flare_table.tex"
    cache:
        True
    script:
        "src/scripts/paper_latex_flare_table.py"
