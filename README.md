# SCF net worth by education

This project plots median family net worth by the education of the family’s reference person, using the Federal Reserve’s Survey of Consumer Finances (SCF) from 1989 through 2025. The current academic-style figure is [`figures/scf_net_worth_by_education_academic.svg`](figures/scf_net_worth_by_education_academic.svg). An earlier figure remains at [`figures/scf_net_worth_by_education.svg`](figures/scf_net_worth_by_education.svg).

## Data and rerunning

[`get_data.py`](get_data.py) downloads the Federal Reserve’s SCF interactive-chart ZIP and extracts `interactive_bulletin_charts_edcl_median.csv` into [`data/scf_education_median_net_worth.csv`](data/scf_education_median_net_worth.csv). Values are thousands of 2025 dollars. Education categories are separate groups; “College degree” means the SCF reference person has a college degree. The SCF family is its primary economic unit, not necessarily everyone in a household.

From this directory, run with Python 3:

```sh
python3 get_data.py
python3 plot.py
```

`get_data.py` refreshes the CSV; `plot.py` reads it and writes the academic-style SVG under `figures/`. Both scripts use only the Python standard library.

## Sanity checks

- The chart’s 2025 college-degree median ($505.03K) is consistent with the Federal Reserve’s published 2025 Table 2 ($505.4K) and standard-error workbook ($505.39K): about $0.37K, or 0.07%, difference.
- The Fed workbook reports a standard error of $33.05K. A rough 95% interval using estimate ± 1.96 standard errors is $440.6K–$570.2K.
- The independent Census SIPP estimate also shows higher wealth at higher education levels: in 2024, median wealth was $323.5K for households where the most educated member had a bachelor’s degree. This is a directional check, not a like-for-like comparison: survey year, unit, education rule, survey design, and wealth definition differ.

Sources: [Federal Reserve SCF chart data](https://www.federalreserve.gov/econres/scf/dataviz/download/zips/scf.zip), [2025 SCF report](https://www.federalreserve.gov/publications/files/scf26.pdf), [2025 SCF standard errors](https://www.federalreserve.gov/econres/files/2025_tables1_2_stderrs.xlsx), and Census Bureau, [*Wealth of Households: 2024*](https://www2.census.gov/library/publications/2026/demo/p70br-218.pdf).
