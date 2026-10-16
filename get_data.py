#!/usr/bin/env python3
"""Download and extract Federal Reserve SCF education median net worth data."""

from __future__ import annotations

import csv
import io
import urllib.request
import zipfile
from pathlib import Path

URL = "https://www.federalreserve.gov/econres/scf/dataviz/download/zips/scf.zip"
SOURCE_MEMBER = "interactive_bulletin_charts_edcl_median.csv"
ROOT = Path(__file__).resolve().parent
OUT = ROOT / "data" / "scf_education_median_net_worth.csv"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        archive = response.read()
    with zipfile.ZipFile(io.BytesIO(archive)) as zf:
        rows = csv.DictReader(io.StringIO(zf.read(SOURCE_MEMBER).decode("utf-8-sig")))
        fields = ["year", "Category", "Net_Worth"]
        with OUT.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow({field: row[field] for field in fields})
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
