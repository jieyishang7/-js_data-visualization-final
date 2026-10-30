# Source guide: Pixar and Disney Animation

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

### TMDB user reviews — planned source

TMDB user reviews are planned for a later stage to explore growth, family, loss and explicitly described rewatch experiences in reviews of selected Pixar and Disney Animation films. No TMDB reviews have been downloaded or analyzed; sample size, film coverage and data dimensions remain unverified.

- Source/producer: The Movie Database (TMDB), user-contributed reviews.
- Documentation consulted: October 30, 2026.
- [Official movie reviews API](https://developer.themoviedb.org/reference/movie-reviews): `GET /3/movie/{movie_id}/reviews`, supporting language and pagination.
- [API application](https://www.themoviedb.org/settings/api): an account and API credentials are required.
- [Official use conditions](https://developer.themoviedb.org/docs/faq): non-commercial API use is free with required attribution, approved logo and the notice “This product uses the TMDB API but is not endorsed or certified by TMDB.” Follow the API terms; access does not imply unrestricted redistribution of third-party review text. Keep credentials out of GitHub.

Before analysis, check review counts per film, available fields, missing values, duplicate IDs, dates and language coverage. Theme labels will be project-created annotations. Viewer age cannot be inferred, and TMDB reviews must not be described as IMDb reviews. Publish project-generated summaries; verify applicable rights before publishing any raw review corpus.
