#!/usr/bin/env python3
"""Create an academic-style SCF net-worth figure from the prepared SCF data."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "scf_education_median_net_worth.csv"
OUT = ROOT / "figures" / "scf_net_worth_by_education_academic.svg"

SERIES_STYLE = {
    "College degree": ("#111111", ""),
    "Some college": ("#333333", "10 4"),
    "High school diploma": ("#666666", "4 3"),
    "No high school diploma": ("#888888", "1 4"),
}


def main() -> None:
    series: dict[str, list[tuple[int, float]]] = defaultdict(list)
    with DATA.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            series[row["Category"]].append((int(row["year"]), float(row["Net_Worth"])))
    for points in series.values():
        points.sort()

    width, height = 1120, 700
    left, right, top, bottom = 105, 805, 130, 525
    x_min, x_max, y_max = 1989, 2025, 600
    x = lambda year: left + (year - x_min) / (x_max - x_min) * (right - left)
    y = lambda value: bottom - value / y_max * (bottom - top)
    college_1989 = next(v for year, v in series["College degree"] if year == 1989)
    hs_1989 = next(v for year, v in series["High school diploma"] if year == 1989)
    college_2025 = next(v for year, v in series["College degree"] if year == 2025)
    hs_2025 = next(v for year, v in series["High school diploma"] if year == 2025)
    gap_1989 = college_1989 - hs_1989
    gap_2025 = college_2025 - hs_2025

    out = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="fig-title fig-desc">
<title id="fig-title">Median family net worth by education, 1989–2025</title>
<desc id="fig-desc">Federal Reserve Survey of Consumer Finances estimates of median family net worth by the educational attainment of the reference person. Values are in thousands of 2025 dollars. Four education categories are shown separately.</desc>
<rect width="100%" height="100%" fill="#ffffff"/>
<text x="{left}" y="38" font-family="Georgia, 'Times New Roman', serif" font-size="14" font-weight="700" fill="#111">FIGURE 1</text>
<text x="{left}" y="73" font-family="Georgia, 'Times New Roman', serif" font-size="25" font-weight="700" fill="#111">Median family net worth by education of reference person</text>
<text x="{left}" y="99" font-family="Georgia, 'Times New Roman', serif" font-size="15" fill="#333">United States, 1989–2025 (thousands of 2025 dollars)</text>
''']

    # A compact grayscale legend with line patterns that remain distinct in print.
    legend_x = left
    for category in ("College degree", "Some college", "High school diploma", "No high school diploma"):
        color, dash = SERIES_STYLE[category]
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        out.append(f'<line x1="{legend_x}" y1="116" x2="{legend_x + 28}" y2="116" stroke="{color}" stroke-width="2.7"{dash_attr}/>')
        out.append(f'<text x="{legend_x + 35}" y="120" font-family="Arial, sans-serif" font-size="12" fill="#222">{category}</text>')
        legend_x += {"College degree": 160, "Some college": 145, "High school diploma": 205, "No high school diploma": 0}[category]

    for value in range(0, y_max + 1, 100):
        yy = y(value)
        out.append(f'<line x1="{left}" y1="{yy:.1f}" x2="{right}" y2="{yy:.1f}" stroke="#d5d5d5" stroke-width="0.8"/>')
        out.append(f'<text x="{left - 12}" y="{yy + 4:.1f}" text-anchor="end" font-family="Arial, sans-serif" font-size="12" fill="#222">{value}</text>')

    for year in (1989, 1995, 2001, 2007, 2013, 2019, 2025):
        xx = x(year)
        out.append(f'<line x1="{xx:.1f}" y1="{bottom}" x2="{xx:.1f}" y2="{bottom + 5}" stroke="#222" stroke-width="0.8"/>')
        out.append(f'<text x="{xx:.1f}" y="{bottom + 22}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#222">{year}</text>')

    for category in ("No high school diploma", "High school diploma", "Some college", "College degree"):
        points = series[category]
        color, dash = SERIES_STYLE[category]
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        coords = " ".join(f"{x(year):.1f},{y(value):.1f}" for year, value in points)
        width_px = 3.0 if category == "College degree" else 2.1
        out.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width_px}"{dash_attr}/>')
        for year, value in points:
            # All marks remain visible in monochrome printing.
            radius = 2.5 if year == 2025 else 1.6
            out.append(f'<circle cx="{x(year):.1f}" cy="{y(value):.1f}" r="{radius}" fill="#fff" stroke="{color}" stroke-width="1.2"/>')

    # Right-side direct labels identify each series and its latest estimate.
    label_dy = {"College degree": 5, "Some college": 4, "High school diploma": -5, "No high school diploma": 5}
    for category in ("College degree", "Some college", "High school diploma", "No high school diploma"):
        latest = series[category][-1][1]
        color, _ = SERIES_STYLE[category]
        out.append(f'<text x="{right + 14}" y="{y(latest) + label_dy[category]:.1f}" font-family="Arial, sans-serif" font-size="12" font-weight="700" fill="{color}">{category}: ${latest:.0f}k</text>')

    out.append(f'''<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#222" stroke-width="0.9"/>
<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#222" stroke-width="0.9"/>
<text x="{(left + right) / 2}" y="{bottom + 47}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#111">Survey year</text>
<text transform="translate(34 {(top + bottom) / 2}) rotate(-90)" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" fill="#111">Median net worth (thousands of 2025 dollars)</text>
<text x="{left}" y="{height - 73}" font-family="Georgia, 'Times New Roman', serif" font-size="12" fill="#111"><tspan font-weight="700">Note:</tspan> Family is the SCF primary economic unit; education is that of its reference person.</text>
<text x="{left}" y="{height - 53}" font-family="Georgia, 'Times New Roman', serif" font-size="12" fill="#111">Education groups are separate. The college–high-school median gap increased from ${gap_1989:.0f}k (1989) to ${gap_2025:.0f}k (2025).</text>
<text x="{left}" y="{height - 28}" font-family="Georgia, 'Times New Roman', serif" font-size="11" fill="#444">Source: Board of Governors of the Federal Reserve System, Survey of Consumer Finances; public interactive chart data.</text>
</svg>''')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
