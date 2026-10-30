# Growing Up with Magic

## Final Project Data Report

IMDb and Rotten Tomatoes user reviews are planned for a later stage to explore viewers’ personal experiences and reflections on growing up.

### Project question and scope

How can Pixar's films provide a timeline for exploring growing up, family, friendship, identity, and the stories people revisit at different stages of life? This acquisition report establishes a reproducible film-level foundation: release dates, runtime, rating, genres, reception, and financial context. It does **not** claim that review scores measure emotional impact, nostalgia, or how an individual changes with age. Those questions require separately documented audience research or transparent manual thematic coding. The October 30 Disney catalogue addition is documented separately in section 10; the computed Pixar statistics retain their original scope.

### 1. Sources and acquisition

The primary source is Eric Leung's [pixarfilms](https://github.com/erictleung/pixarfilms), a community-maintained R data package, not an official Pixar dataset. Six linked CSV tables were downloaded on **October 29, 2026 (America/New_York)** by cloning the repository. Snapshot commit: [`e85a10a77b043d45fe8d950dbdf4d27886ccf520`](https://github.com/erictleung/pixarfilms/tree/e85a10a77b043d45fe8d950dbdf4d27886ccf520). Raw files here preserve the upstream bytes. The manifest in `analysis/results.json` records SHA-256 hashes and file sizes.

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

Total download size is **23,668 bytes** across six CSVs, readily manageable on a laptop. No credentials, API keys, or paid services are needed to analyze the saved snapshot.

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
| pixar_franchises | 0 | 0 | 0 | 14 |
| public_response | 0 | 0 | 0 | 0 |
| themes_vox | 0 | not applicable: multi-label table | 2 | 15 |

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

Python 3.9+ standard library only; no installations or network required. This rebuilds this report and `analysis/results.json` from `data/raw/` and `data/disney/`, with the source inventory from `SOURCE_GUIDE.md`. Source files, checksums, missing counts, outlier details, categorical frequencies and temporal summaries are included. `sources/` contains the upstream data dictionary and license. To obtain the identical source again, clone the upstream repository and check out the snapshot commit above, then compare the six Pixar CSV SHA-256 values in the results manifest.

**AI assistance disclosure:** Codex assisted with acquisition, code and report drafting. Statistical results were calculated by executing the included code on the downloaded files. Interpretation and any future theme coding should be reviewed by the student.

### 8. Added datasets: story themes and franchises

Added to the report on October 30, 2026. Both files were already acquired within the upstream repository clone on October 29, 2026, at the same pinned commit as the four primary tables. Original bytes are preserved. Their most recent file commits are August 9, 2026; the next update is not scheduled. These tables describe film-level editorial categories, not viewer geography, age, or emotional responses.

| Dataset | Producer / source | Size | Columns and analytical types | Row unit |
| --- | --- | --- | --- | --- |
| [themes_vox](data/raw/themes_vox.csv) | Eric Leung and contributors, adapting Vox's editorial theme chart | 124 rows × 2 columns | film: string; theme: categorical string | one recorded film–theme annotation |
| [pixar_franchises](data/raw/pixar_franchises.csv) | Eric Leung and contributors, pixarfilms | 17 rows × 2 columns | film: string/key; franchise: categorical string | one film's franchise membership |

Immutable downloads: [themes_vox.csv](https://raw.githubusercontent.com/erictleung/pixarfilms/e85a10a77b043d45fe8d950dbdf4d27886ccf520/data-raw/themes_vox.csv), [pixar_franchises.csv](https://raw.githubusercontent.com/erictleung/pixarfilms/e85a10a77b043d45fe8d950dbdf4d27886ccf520/data-raw/pixar_franchises.csv). Theme provenance: [Vox chart](https://www.vox.com/2015/11/23/9780818/pixar-chart-movies-toy-story-anniversary). The package states CC0; section 3's third-party-rights limitation particularly applies to Vox's wording and editorial selections. Cite Vox when displaying these annotations, distinguish them from this project's own coding, and review reuse terms before reproducing the original chart or its expressive wording. No chart image is included. Upstream dictionaries are archived in `sources/`.

**Theme validation and cleaning:** raw theme titles contain `Bug's Life` and `Monsters, Inc`, which do not exactly match the master film table. The analysis applies two explicit aliases: `Bug's Life` → `A Bug's Life`, and `Monsters, Inc` → `Monsters, Inc.`. It leaves the raw CSV unchanged and deduplicates normalized film–theme pairs for counts. Repeated film names are expected in this multi-label table. A missing annotation is treated as unknown, not as an absent theme. This historical editorial chart includes Finding Dory, whose release followed the original 2015 article date; its annotations should be checked against the original chart and any later updates before interpreting them as retrospective coding.

Raw unique title strings: **18**; after normalization: **17 films**, **124 unique pairs**, **12 theme labels**; duplicate pairs after normalization: **0**; unmatched normalized titles: **0**. Mapped release coverage: **1995-11-22–2016-06-17**.

| Editorial theme | Films with recorded annotation | Percent of covered films |
| --- | --- | --- |
| An ad hoc community is formed by movie's end | 14 | 82.35 |
| Someone finds their calling | 14 | 82.35 |
| A mismatched pair of partners | 14 | 82.35 |
| And a wacky ensemble of supporting players | 13 | 76.47 |
| Go on a wacky journey | 13 | 76.47 |
| We explore the hidden world of everyday objects | 12 | 70.59 |
| A child comes of age | 11 | 64.71 |
| A loved one is lost | 9 | 52.94 |
| With serious philosophical differences | 8 | 47.06 |
| Their parent figure realizes nothing lasts forever | 7 | 41.18 |
| There's a super sad piece of music | 7 | 41.18 |
| Cars can talk | 2 | 11.76 |

Number of recorded themes per covered film (not a measure of narrative complexity):

| n | Min | Max | Mean | Median | Range | Sample SD | 25% | 75% |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 17 | 5 | 11 | 7.29 | 6 | 6 | 2.17 | 6.00 | 9.00 |

Films without any theme records: Cars 3, Coco, Elemental, Elio, Hoppers, Incredibles 2, Inside Out 2, Lightyear, Luca, Onward, Soul, Toy Story 4, Toy Story 5, Turning Red. These remain unannotated; no labels are inferred.

**Franchise statistics and validation:** all 17 film keys match the master table. There are six recorded franchises. Franchise membership includes originals, sequels, prequels and a spin-off (Lightyear), so the table below measures intervals between franchise releases, not exclusively sequel waiting times. Films without membership records are described as unlisted rather than automatically classified as standalone.

| Franchise | Recorded films | First release | Latest release | Span (days) |
| --- | --- | --- | --- | --- |
| Cars | 3 | 2006-06-09 | 2017-06-16 | 4025 |
| Finding Nemo | 2 | 2003-05-30 | 2016-06-17 | 4767 |
| Inside Out | 2 | 2015-06-19 | 2024-06-14 | 3283 |
| Monsters, Inc. | 2 | 2001-11-02 | 2013-06-21 | 4249 |
| The Incredibles | 2 | 2004-11-05 | 2018-06-15 | 4970 |
| Toy Story | 6 | 1995-11-22 | 2026-06-19 | 11167 |

Adjacent-release gaps within recorded franchises (days):

| n | Min | Max | Mean | Median | Range | Sample SD | 25% | 75% |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11 | 1092 | 4970 | 2951 | 3283 | 3878 | 1,407.59 | 1,652.00 | 4,054.00 |

Unlisted films: A Bug's Life, Brave, Coco, Elemental, Elio, Hoppers, Luca, Onward, Ratatouille, Soul, The Good Dinosaur, Turning Red, Up, WALL-E.

**Use in Growing Up with Magic:** combine themes with release dates for an annotated movie–theme matrix; use franchise timelines to show how characters return across life stages. A reader-entered birth year could produce their age at each release, explicitly labeled as calculated age at release rather than age at first viewing. Neither dataset establishes that themes changed audience emotions or measures the same person over time. Before a full 31-film theme visualization, develop a coding rubric and fill coverage gaps through documented manual review.

### 9. IMDb official data: documented prospective source

**Source / producer:** IMDb.com, Inc. **Accessed:** October 30, 2026. [IMDb Data](https://data.imdb.com/) describes licensed metadata products. The relevant public subset is documented separately under [IMDb Non-Commercial Datasets](https://data.imdb.com/non-commercial-datasets/), with files at [datasets.imdbws.com](https://datasets.imdbws.com/).

**Acquisition status:** documentation reviewed; official IMDb bulk files have **not** been downloaded or analyzed for this report. No official-file row counts, file sizes, descriptive statistics or validation findings are claimed. Existing IMDb scores in sections 4–5 came from the pinned pixarfilms CSV, not a direct IMDb bulk download. The [user-supplied Pixar list](https://www.imdb.com/list/ls087911008/) is a separate browsing reference; its membership has not been independently validated or imported.

| Candidate file | Documented columns | Intended project use |
| --- | --- | --- |
| title.basics.tsv.gz | 9: tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres | match film IDs and check titles, years, runtime and genre |
| title.ratings.tsv.gz | 3: tconst, averageRating, numVotes | obtain an explicitly dated rating and vote-count snapshot |
| title.crew.tsv.gz | 3: tconst, directors, writers | optional creator comparisons using person IDs |

**Format and structure:** gzipped UTF-8 TSV with a header; the backslash-N marker (`\N`) denotes missing values. `tconst` is a title identifier/string and a potential join key. Title text and titleType are strings; years and runtime are nullable integers; isAdult is a boolean flag, not an MPA age rating; genres is a multi-value field. averageRating is numeric and numVotes is an integer. Directors and writers are arrays of person identifiers. These files cover broad IMDb title records, not an already filtered Disney/Pixar film collection. Select the project films using a verified catalogue and match by ID, title and year rather than assuming a genre or company-name filter identifies the correct population.

**Updates and limits:** IMDb states that the public files refresh daily. No particular snapshot timestamp has been acquired here. The documented public files do not include plot summaries, user-review text, viewer age groups, emotional themes or a Disney/Pixar studio-membership column. Those would require separately permitted sources or documented manual coding. Browsing an IMDb page is not equivalent to downloading a dataset.

**Terms and attribution:** this is copyrighted data under limited personal/non-commercial terms, not CC0 or unrestricted open data. See [IMDb non-commercial use guidance](https://help.imdb.com/article/imdb/general-information/can-i-use-imdb-data-in-my-software/G5JTRESSHJBBHTGX) and [Conditions of Use](https://www.imdb.com/conditions/). The guidance restricts republishing/recreating a movie database and automated website extraction, and requires the statement: “Information courtesy of IMDb (https://www.imdb.com). Used with permission.” These restrictions must be checked before using a future extract in a public repository or website. No IMDb bulk extract or review corpus is redistributed in this repository.

**Planned validation if acquired:** record download date, dimensions and checksums; test unique/nonmissing tconst keys, title/year matches, missing-value parsing, score ranges, nonnegative vote counts and unmatched project titles. Preserve a matching log and distinguish live IMDb ratings from the older pixarfilms snapshot. This is a future validation plan, not a claim that these checks have already been performed on IMDb bulk files.

### 10. Disney official film catalogue: acquired and analyzed

**Dataset:** Walt Disney Animation Studios film catalogue, project-compiled factual extract. **Producer:** Walt Disney Animation Studios (source), extraction by this project. **Source:** [official Feature Films page](https://disneyanimation.com/films/). **Access/download date:** October 30, 2026. **Download:** [data/disney/disney_films.csv](data/disney/disney_films.csv). This is a separate dataset added after the original October 29 Pixar submission. The downloaded HTML was successfully parsed; the acquisition byte count and hash are in [sources/disney_acquisition.json](sources/disney_acquisition.json). HTML, images and synopses are not republished.

Each row is a film card appearing in the official catalogue grid. The featured upcoming Hexed promotional banner is excluded because it is outside that grid and its stated November 25, 2026 release is after acquisition. This rule describes a reproducible page extract; it is not a claim that every Disney release, short, subsidiary or distribution title is included. Pixar remains a separate studio dataset.

| Column | Analytical type | Definition |
| --- | --- | --- |
| film | string | displayed film title |
| release_year | integer | year shown on its catalogue card; not an exact premiere date |
| studio | categorical string | Walt Disney Animation Studios, fixed by the catalogue scope |
| source_url | string/URL | film's official page and source join key |
| access_date | ISO date | project acquisition date, not a release date |

**Actual size:** 64 rows × 5 columns; 7,329 bytes. **Coverage:** 1937–2025. Geography: studio film catalogue, not a regional audience dataset; the card years do not identify country-specific releases. The source page does not provide a reliable dataset update timestamp or fixed next update. Recheck when the studio releases films; access date must not be described as last update.

**Computed release-year statistics** (calendar year is a temporal coordinate; its mean is not average film age):

| n | Min | Max | Mean | Median | Range | Sample SD | 25% | 75% |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 64 | 1937 | 2025 | 1,986.27 | 1,994.50 | 88 | 27.43 | 1,960.50 | 2,008.25 |

**Films by decade:**

| Decade | Films | Percent |
| --- | --- | --- |
| 1930s | 1 | 1.56 |
| 1940s | 10 | 15.62 |
| 1950s | 5 | 7.81 |
| 1960s | 3 | 4.69 |
| 1970s | 4 | 6.25 |
| 1980s | 5 | 7.81 |
| 1990s | 9 | 14.06 |
| 2000s | 12 | 18.75 |
| 2010s | 9 | 14.06 |
| 2020s | 6 | 9.38 |

**Validation and remedies:**

| Check | Actual finding |
| --- | --- |
| Missing cells | 0 |
| Exact duplicate rows | 0 |
| Duplicate titles | 0 |
| Duplicate official URLs | 0 |
| Release years after 2026 | 0 |
| Source years descending | True |

The year field was required to match four digits during extraction. Chronological gaps are expected because the studio did not release a grid-listed film every year; they are not missing rows inferred by the analysis. Early and late dates are retained, not removed as outliers. Only years are available in this extract, so within-year order, exact release intervals and country-specific premieres remain unknown. Keep the catalogue title and URL when matching IMDb/Pixar tables and manually review title variants. There are no plot summaries, reviews, emotional labels or viewer ages in this dataset. The catalogue supports the Disney side of the project timeline; theme coding remains a separate task.

**Rights:** the source displays Disney's all-rights-reserved copyright notice; no open-data licence was identified on the catalogue page. This project attributes Disney and publishes only a small factual title/year list and source links, not the copyrighted page design, images or descriptive prose. Do not label this extract CC0 or treat it as permission to reproduce Disney assets. Review [Disney terms](https://disneytermsofuse.com/) for any expanded reuse. The upstream Pixar package's CC0 licence does not apply to this new source.

**Reproduction:** the main analysis reads the saved CSV offline and regenerates its statistics and report. For a new acquisition, download the official page separately and run `python3 analysis/disney.py --from-html /path/to/films.html`. This refresh changes the snapshot and must be reviewed before replacing saved data.

### 11. Disney family-theme research: conceptual reference

Tanner, L. R., Haddock, S. A., Zimmerman, T. S., & Lund, L. K. (2003). *Images of Couples and Families in Disney Feature-Length Animated Films*. The American Journal of Family Therapy, 31(5), 355–373. [DOI and publisher page](https://doi.org/10.1080/01926180390223987). The journal issue year is 2003; the publisher separately lists an online publication date of March 22, 2012.

**Accessed:** October 30, 2026 (publisher abstract/metadata previously inspected, current direct automated access returned 403). The abstract describes analysis of 26 Disney animated films and identifies patterns concerning the importance of family, simplified family diversity, unequal parental portrayals and romantic relationship conventions. These ideas can inform a future coding rubric for family relationships; they are not a validated crosswalk to the Vox labels.

**Status:** literature reference only. Full text and original row-level coding data have not been acquired. The 26-film count is reported by the abstract, not independently computed here. No film-by-film labels, data dimensions, statistics or replication claims are inferred from it. Check the full methods and film sample through university library access before adapting its framework. The paper's earlier historical scope cannot establish patterns for newer films.

**Rights:** link and cite the paper; no open dataset licence was verified and no PDF, tables or coded dataset is redistributed. Any new annotations created for this project should have their own rubric, evidence, author and date, and be distinguished from the authors' findings.

### 12. Updated source inventory and studio classification

**Pixar and Disney Animation source guide**

Reviewed October 30, 2026. This guide separates acquired evidence from references and candidates. A link in this document does not mean its data has been downloaded or validated.

## Scope and studio classification

Use **production studio**, rather than Disney ownership, distribution, genre or a fan list, to define the two comparison groups.

| Group | Project definition | Examples | Acquired data |
| --- | --- | --- | --- |
| Pixar | Pixar Animation Studios feature films in the saved pixarfilms snapshot | Toy Story, WALL-E, Brave, Inside Out | 31 films; six linked CSV tables in `data/raw/` |
| Disney Animation | Walt Disney Animation Studios catalogue grid, including historical studio names | Snow White, The Lion King, Frozen, Moana | 64 title/year records, 1937–2025, in `data/disney/disney_films.csv` |
| Other Disney-related productions | Disney live action, remakes, DisneyToon, television, Marvel and Lucasfilm | Not automatically part of either group | Outside the core comparison; require separate verified labels if added |

Pixar belongs to the Disney corporate family but remains a separate analytical group. *Brave* belongs to Pixar; *Frozen* belongs to Disney Animation. An article using “Disney” broadly may mix these groups. Preserve the original source title, year and identifier during matching. Do not merge on title alone or count a Pixar film twice.

## Pixar: acquired datasets

All six files below come from [Eric Leung and contributors' pixarfilms package](https://github.com/erictleung/pixarfilms), snapshot `e85a10a77b043d45fe8d950dbdf4d27886ccf520`. The package carries CC0; see the saved licence and report for third-party limitations. Counts below were computed from local CSVs.

| File | Rows × columns | Purpose |
| --- | --- | --- |
| [pixar_films.csv](data/raw/pixar_films.csv) | 31 × 6 | Film identity, release, runtime, certificate and synopsis |
| [public_response.csv](data/raw/public_response.csv) | 31 × 17 | Aggregate ratings and participation measures |
| [box_office.csv](data/raw/box_office.csv) | 31 × 5 | Budgets and theatrical receipts |
| [genres.csv](data/raw/genres.csv) | 228 × 3 | Multi-label genre records |
| [themes_vox.csv](data/raw/themes_vox.csv) | 124 × 2 | Editorial story labels, covering 17 films after title normalization |
| [pixar_franchises.csv](data/raw/pixar_franchises.csv) | 17 × 2 | Six franchise groups, including spin-offs |

The Vox labels describe selected films and are not audience survey results. Coverage stops in 2016; absence of a row does not mean absence of a theme. Do not extend these labels to Disney films or newer Pixar films without separate evidence and coding. Detailed computed statistics, missingness, outliers and title remedies are in [DATA_REPORT.md](DATA_REPORT.md).

## Disney Animation: acquired catalogue and research references

| Source | What it contributes | Status and limits |
| --- | --- | --- |
| [Official Disney Animation films](https://disneyanimation.com/films/) | Studio-defined title/year population for the Disney timeline | **Acquired and analyzed:** 64 × 5 factual extract; no images or synopsis prose republished. No open-data licence identified. Exact premiere dates, viewer ages and themes are absent. |
| [Tanner et al. (2003), Images of Couples and Families](https://doi.org/10.1080/01926180390223987) | Family and relationship concepts for designing a coding rubric | **Literature reference:** abstract/metadata reviewed; full methods and row-level data not acquired. Report section 11 records this distinction. No paper or tables redistributed. |
| [Izarra de Luna & Gelado Marcos (2024), Disney Reloaded](https://www.mdpi.com/2673-5172/5/4/91) | Character arcs, personality, plot and relationships in Disney Animation | **Article and selected appendix inspected:** useful research framework, not a Pixar film dataset. See below. |
| [DeeDee Studio, animated characters](https://www.deedeestudio.net/en/post/animated-characters) | Editorial interpretations of life lessons and character development | **Context only:** article reviewed; mixes studios, including Pixar's Brave. Any future tags must be labelled project interpretation, with film-specific evidence. No structured dataset acquired or article text copied. |
| [CBR life lessons article](https://www.cbr.com/life-lessons-disney-animation-films/) | Possible additional editorial examples | **Unverified candidate:** automated retrieval failed; no claims or labels extracted. Keep as a reading lead, not analytical evidence. |
| [Disney Wiki](https://disney.fandom.com/wiki/The_Disney_Wiki) | Community reference for film/character links and source discovery | **Secondary reference:** not an official studio catalogue. Verify individual entries and citations; broad Disney scope can include Pixar and other labels. No wiki corpus acquired. Check page-specific licences and media exceptions before reuse. |

### Disney Reloaded: verified research details

Marta Izarra de Luna and Roberto Gelado Marcos, *Journalism and Media* 5(4), 1452–1476 (2024), [doi:10.3390/journalmedia5040091](https://doi.org/10.3390/journalmedia5040091). Published September 25, 2024; inspected October 30, 2026. The article is CC BY 4.0; third-party assets need separate checking.

Its methods describe 23 selected Disney Animation films across two periods around the 2006 Pixar acquisition, excluding Fantasia 2000 and Winnie the Pooh. The historical range in the title is 1994–2018. The study concerns Disney films; acquisition is the comparison boundary, not a label making those films Pixar productions.

Appendix D, Table A3 reports character-arc counts: before, inexistent/change/growth/fall = 4/6/4/0; after = 2/1/6/0. These are **published aggregate counts**, not newly coded films. The appendix footnote still lists Winnie the Pooh although the methods exclude it: reconcile the film roster before extracting a film-level dataset. The data statement points to contributions within the article and author inquiries; no separate downloadable CSV/Excel matrix was verified. No published tables or full text are redistributed here.

This supports a future coding framework, not a causal claim about the acquisition or evidence of viewers changing with age. The project's current CSV statistics do not include this paper's coded observations.

## Sources that can serve both studios: prospective, not yet analyzed

| Source | Potential use | Acquisition / rights / limitations |
| --- | --- | --- |
| [IMDb public datasets](https://data.imdb.com/non-commercial-datasets/) and [data portal](https://data.imdb.com/) | IDs, titles, years, runtimes, genres and aggregate ratings | Documented in report section 9; bulk files not acquired here. Daily refresh; limited non-commercial terms. No review text, plot summaries, emotional labels or viewer age in the public files. Do not redistribute a bulk extract without checking terms. |
| [User-supplied Pixar IMDb list](https://www.imdb.com/list/ls087911008/) and [Disney list](https://www.imdb.com/list/ls026785255/) | Candidate title checking | User-created lists, not official studio populations or downloaded datasets. Verify membership against studio sources. |
| [TMDB API](https://developer.themoviedb.org/docs/getting-started) | Film overviews; available user reviews through separate movie endpoints | No API collection performed. Requires credentials and compliance with attribution/use terms. Review availability varies; neither review text nor ratings establish viewer age. |
| [MovieLens 1M](https://files.grouplens.org/datasets/movielens/ml-1m-README.txt) | Historical film ratings linked to user age brackets | Documentation lead; not incorporated or computed here. Older coverage limits recent films; age is the historical user bracket, not age at first viewing. Check GroupLens terms, including redistribution, before acquisition/publication. |
| [Disney API](https://disneyapi.dev/) | Character-to-film relationships | Community character API, not an official theme or audience dataset. No records acquired or licence for a saved extract verified. |
| [Keith Galli Disney data project](https://github.com/KeithGalli/disney-data-science-tasks) | Broader Disney film metadata and Wikipedia-derived information | Candidate only; scope includes live action and other productions. Verify current file, provenance, studio labels and redistribution rights before using. No local analysis or open data licence claimed here. |
| [Disney story-themes thesis supplied by user](https://repository.rit.edu/cgi/viewcontent.cgi?article=10429&context=theses) | Potential scholarly context | Bibliographic lead only: contents and underlying dataset not verified, so no findings are attributed to it. |

## Evaluated and excluded from real-data analysis

- [crystalbaby / The Disney Movies Dataset](https://www.kaggle.com/datasets/crystalbaby/the-disney-movies-dataset): its data card explicitly identifies programmatically generated **synthetic data**, mixing recognizable franchises with invented titles and future releases. The publisher describes 1,000 rows, 76 columns and 1937–2027 coverage; those are source-reported dimensions, not local computed results. The card lists Apache 2.0. Synthetic ratings, rewatch scores and target age groups cannot establish real audience behaviour or actual film history. **Do not merge it into the project.** No file downloaded or redistributed.
- [Disney Animation data sets](https://www.disneyanimation.com/data-sets/): graphics/research resources, not the film/theme table needed here. Not part of the acquired analytical data.

## Recommended visualization and remaining evidence

Use separate Pixar and Disney Animation lanes for the release timeline. Pixar supports richer metadata and the limited Vox theme table; Disney currently supports titles and years. Show these unequal coverage levels explicitly rather than comparing theme percentages with different coding rules.

For a cross-studio theme matrix, select a manageable film sample and create new documented annotations: film identifier, studio, theme, definition, evidence locator, coder, coding date and review status. Treat growing up, family, loss, belonging and identity as proposed categories until coded. Mark unavailable evidence as unknown rather than zero. Paper character-arc categories are not automatically equivalent to Vox themes.

Viewer comments can supply attributed qualitative examples, summarized in the student's own words with original review links. A consistent sampling rule should include mixed responses rather than only favourite comments. Actual age and rewatch experience must be explicitly self-reported; do not infer them from usernames, film certificates or emotional wording. No review corpus has been collected. A birth-year timeline can show age at film release, but must not call that age at first viewing.

Only acquired local files are covered by the computed statistics. References, planned API queries, and published study results remain separately labelled.
