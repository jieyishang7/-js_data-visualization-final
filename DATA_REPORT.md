# Growing Up with Magic: The Stories That Grow with Us

## Final Project Data Report

Columbia Data Visualization · Jieyi Shang · October 29, 2026

### Project question and scope

How can Pixar's films provide a timeline for exploring growing up, family, friendship, identity, and the stories people revisit at different stages of life? This acquisition report establishes a reproducible film-level foundation: release dates, runtime, rating, genres, reception, and financial context. It does **not** claim that review scores measure emotional impact, nostalgia, or how an individual changes with age. Those questions require separately documented audience research or transparent manual thematic coding. Disney data is excluded to keep definitions and provenance consistent.

### 1. Sources and acquisition

The primary source is Eric Leung's [pixarfilms](https://github.com/erictleung/pixarfilms), a community-maintained R data package, not an official Pixar dataset. Four linked CSV tables were downloaded on **October 29, 2026 (America/New_York)** by cloning the repository. Snapshot commit: [`e85a10a77b043d45fe8d950dbdf4d27886ccf520`](https://github.com/erictleung/pixarfilms/tree/e85a10a77b043d45fe8d950dbdf4d27886ccf520). Raw files here preserve the upstream bytes. The manifest in `analysis/results.json` records SHA-256 hashes and file sizes.

| Table / local download | Rows | Columns | Bytes | Row represents | Last file commit date |
| --- | --- | --- | --- | --- | --- |
| [pixar_films](data/raw/pixar_films.csv) | 31 | 6 | 6453 | One film | 2026-08-09 |
| [public_response](data/raw/public_response.csv) | 31 | 17 | 2743 | One film | 2026-08-09 |
| [box_office](data/raw/box_office.csv) | 31 | 5 | 1611 | One film | 2026-08-07 |
| [genres](data/raw/genres.csv) | 228 | 3 | 6793 | One film–category–value assignment | 2026-08-07 |

All four tables were produced/compiled by Eric Leung and contributors. Individual table descriptions and immutable download links:

- **pixar_films:** Release order, release dates, runtime, MPA rating and brief plot. Wikipedia provides order/title/date; OMDb provides runtime/rating/plot. [Original CSV](https://raw.githubusercontent.com/erictleung/pixarfilms/e85a10a77b043d45fe8d950dbdf4d27886ccf520/data-raw/pixar_films.csv).
- **public_response:** Critic and audience reception from Rotten Tomatoes, Metacritic, CinemaScore, IMDb and Letterboxd, compiled in the package. [Original CSV](https://raw.githubusercontent.com/erictleung/pixarfilms/e85a10a77b043d45fe8d950dbdf4d27886ccf520/data-raw/public_response.csv).
- **box_office:** Budget and territorial/worldwide box-office gross in nominal USD, compiled from the package’s Wikipedia source. [Original CSV](https://raw.githubusercontent.com/erictleung/pixarfilms/e85a10a77b043d45fe8d950dbdf4d27886ccf520/data-raw/box_office.csv).
- **genres:** Multiple genre and subgenre labels per film; upstream documentation identifies OMDb as source. [Original CSV](https://raw.githubusercontent.com/erictleung/pixarfilms/e85a10a77b043d45fe8d950dbdf4d27886ccf520/data-raw/genres.csv).

Total download size is **17,600 bytes** across four CSVs, readily manageable on a laptop. No credentials, API keys, or paid services are needed to analyze the saved snapshot.

**Coverage:** 1995-11-22 through 2026-06-19, 31 films. This is a Pixar film collection, not a global sample of animation or a sample of viewers. MPA ratings are US classifications. Box office separates US/Canada and other territories, with worldwide totals. Reception websites aggregate their own users/critics and do not supply viewer geography or demographics here. Release dates follow the upstream list and should not be interpreted as every country's premiere date.

**Updates:** dates above are the most recent Git commits touching each CSV, not per-observation measurement timestamps. The repository's latest commit is August 20, 2026. The CSVs have no observation-level retrieval dates, and scores/grosses may lag the access date. No fixed next-update date is promised in the inspected documentation. Recheck upstream before the final visualization and preserve a new snapshot if refreshed. Upstream `.Rd` documentation is saved in `sources/`; its box-office dimensions are stale (24 rows), so this report uses actual CSV dimensions.

### 2. Schema and joining

CSV stores text; the following are analytical types. `NA` is parsed as missing, never zero. `film` is the exact title join key. Films, response and box office are one-to-one. Genres is one-to-many; aggregate genre membership before joining numerical measures to avoid multiplying a film's gross or score.

| Table | Columns | Analytical type | Meaning / unit |
| --- | --- | --- | --- |
| pixar_films | number | integer | release-order identifier, not a continuous measurement |
| pixar_films | film | string/key | film title |
| pixar_films | release_date | ISO date | upstream release date |
| pixar_films | run_time | integer | minutes |
| pixar_films | film_rating | categorical | MPA classification |
| pixar_films | plot | text | short synopsis; some are truncated |
| box_office | film | string/key | film title |
| box_office | budget; box_office_us_canada; box_office_other; box_office_worldwide | nullable integer | nominal USD; budget is production budget, not total costs |
| genres | film; category; value | strings / categorical | film and Genre/Subgenre label; multi-label |
| public_response | film | string/key | film title |
| public_response | rotten_tomatoes_score; metacritic_score; rotten_tomatoes_score_top_critics; rotten_tomatoes_popcorn_meter_score; rotten_tomatoes_popcorn_meter_verified | nullable numeric | scores on 0–100 scales; definitions differ across sites |
| public_response | imdb_score | decimal | 0–10 observed scale; upstream Rd incorrectly says out of 100 |
| public_response | letterboxd_rating | decimal | 0–5 scale |
| public_response | cinema_score | nullable ordinal category | letter grade; do not average as a number |
| public_response | rotten_tomatoes_counts; metacritic_counts; imdb_counts; rotten_tomatoes_score_top_critics_votes; rotten_tomatoes_popcorn_meter_votes; rotten_tomatoes_popcorn_meter_verified_votes; letterboxd_counts; letterboxd_num_fans | nullable integer | review/vote/fan counts as supplied; rounded audience vote values may be thresholds rather than exact counts |

### 3. License and permitted use

The upstream repository includes [CC0 1.0 Universal](https://github.com/erictleung/pixarfilms/blob/e85a10a77b043d45fe8d950dbdf4d27886ccf520/LICENSE.md), preserved in [sources/PIXARFILMS-LICENSE.md](sources/PIXARFILMS-LICENSE.md). CC0 dedicates the contributor's applicable rights to the public domain to the extent possible, with a fallback license. It permits modification, redistribution and commercial use without an attribution condition. Academic attribution is nevertheless supplied here: **Eric Leung and contributors, pixarfilms, snapshot e85a10a, accessed October 29, 2026**.

CC0 does not clear third-party rights or trademarks. The package combines facts and text obtained from external sites; the upstream license does not establish that all source-site prose or media has been independently cleared. This project redistributes the package's small CSV snapshot under its stated license, keeps source credit, and uses numerical facts for analysis. It includes no film stills, posters, scripts or audio. Avoid reproducing plot text in a public visualization without reviewing its original terms. Relevant source documentation: [Wikipedia](https://en.wikipedia.org/wiki/List_of_Pixar_films), [OMDb](https://www.omdbapi.com/), and the archived upstream schema files in `sources/`. No fresh scraping of review platforms was performed.

### 4. Computed descriptive statistics

All following quantities are computed from the saved CSVs by [analysis/analyze.py](analysis/analyze.py), not copied from a description. Missing observations are omitted variable by variable; `n` shows the denominator. SD is sample standard deviation (n−1). Quantiles use linear interpolation at index (n−1)p. Skewness is the third population central moment divided by variance to the power 1.5. Values are rounded to two decimals only for display. Box-office and budget values below are in **millions of nominal US dollars**, without inflation adjustment.

| Variable (unit) | n | Min | Max | Mean | Median | Range | SD | 25% | 75% | Skewness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| run_time (minutes) | 31 | 81.00 | 118.00 | 100.48 | 100.00 | 37.00 | 7.68 | 95.50 | 104.00 | 0.27 |
| rotten_tomatoes_score (0–100) | 31 | 40.00 | 100.00 | 88.48 | 94.00 | 60.00 | 12.82 | 81.50 | 96.50 | -1.98 |
| metacritic_score (0–100) | 31 | 57.00 | 96.00 | 77.42 | 78.00 | 39.00 | 12.29 | 67.50 | 88.00 | -0.06 |
| imdb_score (0–10) | 31 | 6.10 | 8.40 | 7.50 | 7.50 | 2.30 | 0.65 | 7.15 | 8.10 | -0.37 |
| letterboxd_rating (0–5) | 31 | 2.70 | 4.20 | 3.64 | 3.70 | 1.50 | 0.40 | 3.30 | 4.05 | -0.28 |
| budget (million USD) | 30 | 30.00 | 250.00 | 163.20 | 175.00 | 220.00 | 51.49 | 150.00 | 200.00 | -1.10 |
| box_office_worldwide (million USD) | 31 | 21.81 | 1,698.86 | 601.70 | 528.77 | 1,677.05 | 383.74 | 373.59 | 836.13 | 0.74 |

**Outliers:** values strictly outside Q1−1.5×IQR or Q3+1.5×IQR are flags for review, not automatic errors.

| Variable | Lower fence | Upper fence | Flagged films and values |
| --- | --- | --- | --- |
| pixar_films.run_time | 82.75 | 116.75 | Toy Story: 81.00; Incredibles 2: 118.00 |
| public_response.rotten_tomatoes_score | 59.00 | 119.00 | Cars 2: 40.00 |
| public_response.metacritic_score | 36.75 | 118.75 | None |
| public_response.imdb_score | 5.73 | 9.52 | None |
| public_response.letterboxd_rating | 2.17 | 5.17 | None |
| box_office.budget | 75.00 | 275.00 | Toy Story: 30.00; A Bug's Life: 40.00 |
| box_office.box_office_worldwide | -320.20 | 1,529.92 | Inside Out 2: 1698.86 |

Positive skew means a longer upper tail; negative skew means a longer lower tail. Critic and audience scores are bounded and should be compared on their own scales. A negative score skew can reflect a concentration of highly rated films. Nominal revenue differences also reflect inflation, release strategy, and market conditions, not only popularity.

**Categorical distributions**

**pixar_films.film_rating** (denominator 31 rows; missing shown separately):

| Category | Count | Percent of all rows |
| --- | --- | --- |
| PG | 18 | 58.06 |
| G | 13 | 41.94 |
| Missing | 0 | 0.00 |

**public_response.cinema_score** (denominator 31 rows; missing shown separately):

| Category | Count | Percent of all rows |
| --- | --- | --- |
| A | 18 | 58.06 |
| A+ | 7 | 22.58 |
| A- | 3 | 9.68 |
| Missing | 3 | 9.68 |

**genres.category** (denominator 228 rows; missing shown separately):

| Category | Count | Percent of all rows |
| --- | --- | --- |
| Subgenre | 135 | 59.21 |
| Genre | 93 | 40.79 |
| Missing | 0 | 0.00 |

**Genre/subgenre frequencies** (top 12 assignments; multi-label shares need not sum to 100%):

| Label | Assignments | Percent of 31 films |
| --- | --- | --- |
| Adventure | 31 | 100.00 |
| Animation | 31 | 100.00 |
| Computer Animation | 31 | 100.00 |
| Comedy | 24 | 77.42 |
| Fantasy | 16 | 51.61 |
| Urban Adventure | 9 | 29.03 |
| Supernatural Fantasy | 7 | 22.58 |
| Animal Adventure | 6 | 19.35 |
| Quest | 6 | 19.35 |
| Coming-of-Age | 6 | 19.35 |
| Buddy Comedy | 5 | 16.13 |
| Action | 5 | 16.13 |

**Temporal distribution**

| Release year | Films |
| --- | --- |
| 1995 | 1 |
| 1998 | 1 |
| 1999 | 1 |
| 2001 | 1 |
| 2003 | 1 |
| 2004 | 1 |
| 2006 | 1 |
| 2007 | 1 |
| 2008 | 1 |
| 2009 | 1 |
| 2010 | 1 |
| 2011 | 1 |
| 2012 | 1 |
| 2013 | 1 |
| 2015 | 2 |
| 2016 | 1 |
| 2017 | 2 |
| 2018 | 1 |
| 2019 | 1 |
| 2020 | 2 |
| 2021 | 1 |
| 2022 | 2 |
| 2023 | 1 |
| 2024 | 1 |
| 2025 | 1 |
| 2026 | 2 |

| Release month (1–12) | Films |
| --- | --- |
| 3 | 3 |
| 5 | 2 |
| 6 | 18 |
| 11 | 7 |
| 12 | 1 |

The inclusive period spans 32 calendar years. Years with no recorded releases: 1996, 1997, 2000, 2002, 2005, 2014. Adjacent-release gaps: min 98 days, max 1099 days, mean 372.23 days, median 364.00 days, sample SD 207.89 days. These are film-release events, not repeated measurements of the same audience. The final calendar year is partial as of the access date.

### 5. Actual validation findings and remedies

**Completeness:** each column was checked for blank, `NA`, `N/A`, or `null`. Only columns with missing values appear below; all omitted columns have zero missing cells.

| Table | Column | Missing | Percent | Affected films |
| --- | --- | --- | --- | --- |
| box_office | budget | 1 | 3.23 | Luca |
| public_response | cinema_score | 3 | 9.68 | Soul, Luca, Turning Red |
| public_response | rotten_tomatoes_popcorn_meter_verified | 23 | 74.19 | Toy Story, A Bug's Life, Toy Story 2, Monsters, Inc., Finding Nemo, The Incredibles, Cars, Ratatouille, WALL-E, Up, Toy Story 3, Cars 2, Brave, Monsters University, Inside Out, The Good Dinosaur, Finding Dory, Cars 3, Coco, Incredibles 2, Soul, Luca, Turning Red |
| public_response | rotten_tomatoes_popcorn_meter_verified_votes | 23 | 74.19 | Toy Story, A Bug's Life, Toy Story 2, Monsters, Inc., Finding Nemo, The Incredibles, Cars, Ratatouille, WALL-E, Up, Toy Story 3, Cars 2, Brave, Monsters University, Inside Out, The Good Dinosaur, Finding Dory, Cars 3, Coco, Incredibles 2, Soul, Luca, Turning Red |

**Duplicates and join coverage:**

| Table | Exact duplicate rows | Duplicate film keys | Orphan titles | Films without rows |
| --- | --- | --- | --- | --- |
| box_office | 0 | 0 | 0 | 0 |
| genres | 0 | not applicable: multi-label table | 0 | 0 |
| pixar_films | 0 | 0 | 0 | 0 |
| public_response | 0 | 0 | 0 | 0 |

**Type, range, and temporal checks:** 0 numeric parsing errors; 0 negative/impossible numeric values under the documented scale checks; 0 cells with leading/trailing whitespace; 0 release dates after October 29, 2026. All release dates parsed as ISO dates. Sequential release numbers and chronological source order: True. These checks establish internal plausibility, not independent verification of every external fact.

**Financial reconciliation:** 0 films have worldwide gross different from US/Canada plus other territories (exact integer-dollar check). Details: [].

**Text anomalies:** 3 synopses end in an ellipsis: Cars 2, Turning Red, Elio. These are incomplete inputs for thematic text analysis. No missing text was invented.

**Actions applied in this analysis:** raw data is unchanged; missing values are excluded from each variable's statistics; units are explicit; IMDb is analyzed on the observed 0–10 scale; genre counts remain separate from film-level financial/reception statistics. No imputation, outlier removal, or inferred emotional labels were applied.

**Remedies for the final visualization:** retain Luca with a visible missing budget and exclude it only from budget-dependent comparisons. Keep missing CinemaScore/verified-audience scores as unavailable rather than assign zero or infer poor reception. Do not assume missing verified scores occurred randomly. Review outliers against original sources before correction and retain legitimate extremes. Label vote counts as supplied/possibly rounded rather than precise audience sizes. Do not weight films by these counts without validating their meaning. Separate streaming-era films (especially Soul, Luca and Turning Red) when comparing theatrical revenue, and research release strategy before making causal claims. Never equate gross minus production budget with net profit. Reconcile inconsistent source values if found on refresh, preserving a correction log.

### 6. What the data supports and next steps

The data supports a release timeline, film-rating composition, multi-label genre summaries, and contextual comparisons of runtime, reception, and commercial scale. The plot synopses suggest starting points for themes such as belonging and identity, but they do not constitute validated theme annotations. The project should use a written coding rubric, full-source evidence and a second coding pass before charting emotional themes. No claim about an audience growing up with a movie can be established from aggregate review scores alone. Viewer age, repeat viewing and longitudinal responses are absent. Pixar-only selection, platform participation bias, changing review counts, and unequal theatrical release conditions limit generalization.

### 7. Reproduce and audit

From this repository's root, run:

```sh
python3 analysis/analyze.py
```

Python 3.9+ standard library only; no installations or network required. This rebuilds this report and `analysis/results.json` from `data/raw/`. Source files, checksums, missing counts, outlier details, categorical frequencies and temporal summaries are included. `sources/` contains the upstream data dictionary and license. To obtain the identical source again, clone the upstream repository and check out the snapshot commit above, then compare the four CSV SHA-256 values in the results manifest.

**AI assistance disclosure:** Codex assisted with acquisition, code and report drafting. Statistical results were calculated by executing the included code on the downloaded files. Interpretation and any future theme coding should be reviewed by the student.
