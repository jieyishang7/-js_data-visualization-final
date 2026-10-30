# Growing Up with Magic: The Stories That Grow with Us

Columbia Data Visualization final project · Jieyi Shang

**Assignment due: October 29, 2026. Source expansion: October 30, 2026.**

Read the **[Final Project Data Report](DATA_REPORT.md)** for sources, dimensions, licensing, actual computed statistics, validation findings and remedies. The **[Source Guide](SOURCE_GUIDE.md)** explains every source's role and acquisition status.

## Pixar and Disney Animation are separate groups

| Group | Acquired data | Coverage / use |
| --- | --- | --- |
| Pixar Animation Studios | [Six CSVs](data/raw/) for 31 films | Film metadata, reception, finance, genres, franchises; 124 Vox theme records cover 17 normalized film titles |
| Walt Disney Animation Studios | [Official catalogue extract](data/disney/disney_films.csv), 64 × 5 | Titles and years, 1937–2025; separate computed statistics and validation |
| Cross-studio references | [Source Guide](SOURCE_GUIDE.md) | IMDb, TMDB, historical MovieLens and research; acquisition status is stated individually |

Pixar films are not counted again as Disney Animation films. Other Disney-owned or distributed productions are outside the core comparison. The Disney Reloaded paper studies Disney Animation, even though its title mentions Pixar. Its published character-arc counts are research context, not project-coded film labels.

The crystalbaby Kaggle dataset is excluded because its publisher explicitly identifies it as synthetic. No invented ratings, films or viewer ages enter the analysis. Comments, viewer ages and cross-studio emotional themes have not yet been collected or coded.

## Reproduce

```sh
python3 analysis/analyze.py
```

Python 3.9+ standard library only, no dependencies or network. Reads six saved Pixar CSVs, the Disney catalogue CSV and the source guide; rebuilds `DATA_REPORT.md`, `analysis/results.json` and `analysis/disney_results.json`.

## Files and rights

- `data/raw/`: unchanged Pixar package CSV snapshots.
- `data/disney/`: separately attributed factual catalogue extract.
- `analysis/`: executable acquisition/analysis code and machine-readable results.
- `sources/`: upstream schema documentation, package licence and Disney acquisition manifest.
- `SOURCE_GUIDE.md`: Pixar/Disney classification, references, candidates, exclusions and next steps.

Pixar source: Eric Leung and contributors, [pixarfilms](https://github.com/erictleung/pixarfilms), commit `e85a10a77b043d45fe8d950dbdf4d27886ccf520`, accessed October 29, 2026. Disney catalogue accessed October 30. The Pixar package's CC0 licence does not apply to Disney assets or third-party references. No paper PDFs, review corpus, Disney images or raw IMDb bulk data are redistributed.

Codex assisted with acquisition, code and drafting. Project statistics were computed from saved files; published research findings and unacquired sources are explicitly distinguished.

### TMDB user reviews — planned source

TMDB user reviews are planned for a later stage to explore growth, family, loss and explicitly described rewatch experiences in reviews of selected Pixar and Disney Animation films. No TMDB reviews have been downloaded or analyzed; sample size, film coverage and data dimensions remain unverified.

- Source/producer: The Movie Database (TMDB), user-contributed reviews.
- Documentation consulted: October 30, 2026.
- [Official movie reviews API](https://developer.themoviedb.org/reference/movie-reviews): `GET /3/movie/{movie_id}/reviews`, supporting language and pagination.
- [API application](https://www.themoviedb.org/settings/api): an account and API credentials are required.
- [Official use conditions](https://developer.themoviedb.org/docs/faq): non-commercial API use is free with required attribution, approved logo and the notice “This product uses the TMDB API but is not endorsed or certified by TMDB.” Follow the API terms; access does not imply unrestricted redistribution of third-party review text. Keep credentials out of GitHub.

Before analysis, check review counts per film, available fields, missing values, duplicate IDs, dates and language coverage. Theme labels will be project-created annotations. Viewer age cannot be inferred, and TMDB reviews must not be described as IMDb reviews. Publish project-generated summaries; verify applicable rights before publishing any raw review corpus.
