# Growing Up with Magic: The Stories That Grow with Us

Columbia Data Visualization final project · Jieyi Shang

**Assignment due: October 29, 2026**

Read the **[Final Project Data Report](DATA_REPORT.md)** for data sources, dimensions, types, licensing, computed statistics, validation findings, remedies and limitations.

## Reproduce

```sh
python3 analysis/analyze.py
```

Python 3.9+ standard library only. No dependencies or network needed. Rebuilds `DATA_REPORT.md` and `analysis/results.json` from the six downloaded CSVs in `data/raw/`.

## Contents

- `DATA_REPORT.md`: submission document.
- `data/raw/`: unchanged Pixar CSV snapshots.
- `analysis/analyze.py`: reproducible statistical analysis and report generation.
- `analysis/results.json`: detailed machine-readable results and SHA-256 manifest.
- `sources/`: upstream schema documentation and CC0 license.

Data: Eric Leung and contributors, [pixarfilms](https://github.com/erictleung/pixarfilms), commit `e85a10a77b043d45fe8d950dbdf4d27886ccf520`, accessed October 29, 2026. See the report for licensing details and third-party source limitations.

Codex assisted with data acquisition, code, and drafting; all reported statistical results are computed from the saved files.

Added October 30: editorial story themes and franchise membership, with title normalization, categorical summaries and franchise release intervals. See section 8 of the data report.
