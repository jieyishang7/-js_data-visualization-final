"""Validate editorial theme annotations and franchise membership separately."""
from collections import Counter
from datetime import date

def analyze(tables, stats, md):
    films={r['film']:r for r in tables['pixar_films']}
    aliases={"Bug's Life":"A Bug's Life",'Monsters, Inc':'Monsters, Inc.'}
    raw=tables['themes_vox']
    pairs=[(aliases.get(r['film'],r['film']),r['theme']) for r in raw]
    unique=set(pairs)
    covered={f for f,t in unique}
    counts=Counter(t for f,t in unique)
    per_film=Counter(f for f,t in unique)
    franchises=tables['pixar_franchises']
    groups={}
    for r in franchises: groups.setdefault(r['franchise'],[]).append(r['film'])
    spans=[]; gaps=[]
    for name,members in sorted(groups.items()):
        dates=sorted(date.fromisoformat(films[f]['release_date']) for f in members)
        spans.append([name,len(members),str(dates[0]),str(dates[-1]),(dates[-1]-dates[0]).days])
        gaps.extend((b-a).days for a,b in zip(dates,dates[1:]))
    result={'title_aliases':aliases,'raw_theme_rows':len(raw),'raw_unique_titles':len({r['film'] for r in raw}),'normalized_unique_films':len(covered),'normalized_unique_pairs':len(unique),'duplicate_pairs_after_normalization':len(pairs)-len(unique),'theme_counts':dict(counts.most_common()),'theme_counts_per_film':dict(sorted(per_film.items())),'annotations_per_film_stats':stats(list(per_film.values())),'theme_unmatched_titles':sorted(covered-set(films)),'films_without_theme_records':sorted(set(films)-covered),'franchise_counts':{k:len(v) for k,v in groups.items()},'franchise_spans_days':spans,'franchise_adjacent_gaps_days_stats':stats(gaps),'films_without_franchise_records':sorted(set(films)-{r['film'] for r in franchises})}
    text='''
### 8. Added datasets: story themes and franchises

Added to the report on October 30, 2026. Both files were already acquired within the upstream repository clone on October 29, 2026, at the same pinned commit as the four primary tables. Original bytes are preserved. Their most recent file commits are August 9, 2026; the next update is not scheduled. These tables describe film-level editorial categories, not viewer geography, age, or emotional responses.

| Dataset | Producer / source | Size | Columns and analytical types | Row unit |
| --- | --- | --- | --- | --- |
| [themes_vox](data/raw/themes_vox.csv) | Eric Leung and contributors, adapting Vox's editorial theme chart | 124 rows × 2 columns | film: string; theme: categorical string | one recorded film–theme annotation |
| [pixar_franchises](data/raw/pixar_franchises.csv) | Eric Leung and contributors, pixarfilms | 17 rows × 2 columns | film: string/key; franchise: categorical string | one film's franchise membership |

Immutable downloads: [themes_vox.csv](https://raw.githubusercontent.com/erictleung/pixarfilms/e85a10a77b043d45fe8d950dbdf4d27886ccf520/data-raw/themes_vox.csv), [pixar_franchises.csv](https://raw.githubusercontent.com/erictleung/pixarfilms/e85a10a77b043d45fe8d950dbdf4d27886ccf520/data-raw/pixar_franchises.csv). Theme provenance: [Vox chart](https://www.vox.com/2015/11/23/9780818/pixar-chart-movies-toy-story-anniversary). The package states CC0; section 3's third-party-rights limitation particularly applies to Vox's wording and editorial selections. Cite Vox when displaying these annotations, distinguish them from this project's own coding, and review reuse terms before reproducing the original chart or its expressive wording. No chart image is included. Upstream dictionaries are archived in `sources/`.

**Theme validation and cleaning:** raw theme titles contain `Bug's Life` and `Monsters, Inc`, which do not exactly match the master film table. The analysis applies two explicit aliases: `Bug's Life` → `A Bug's Life`, and `Monsters, Inc` → `Monsters, Inc.`. It leaves the raw CSV unchanged and deduplicates normalized film–theme pairs for counts. Repeated film names are expected in this multi-label table. A missing annotation is treated as unknown, not as an absent theme. This historical editorial chart includes Finding Dory, whose release followed the original 2015 article date; its annotations should be checked against the original chart and any later updates before interpreting them as retrospective coding.

'''
    text+=f"Raw unique title strings: **{result['raw_unique_titles']}**; after normalization: **{len(covered)} films**, **{len(unique)} unique pairs**, **{len(counts)} theme labels**; duplicate pairs after normalization: **{len(pairs)-len(unique)}**; unmatched normalized titles: **{len(result['theme_unmatched_titles'])}**. Mapped release coverage: **{min(films[f]['release_date'] for f in covered)}–{max(films[f]['release_date'] for f in covered)}**.\n\n"
    text+=md(['Editorial theme','Films with recorded annotation','Percent of covered films'],[[t,n,100*n/len(covered)] for t,n in counts.most_common()])
    st=result['annotations_per_film_stats']
    text+='\nNumber of recorded themes per covered film (not a measure of narrative complexity):\n\n'+md(['n','Min','Max','Mean','Median','Range','Sample SD','25%','75%'],[[st[k] for k in ['n','min','max','mean','median','range','sd','q1','q3']]])
    text+='\nFilms without any theme records: '+', '.join(result['films_without_theme_records'])+'. These remain unannotated; no labels are inferred.\n'
    text+='\n**Franchise statistics and validation:** all 17 film keys match the master table. There are six recorded franchises. Franchise membership includes originals, sequels, prequels and a spin-off (Lightyear), so the table below measures intervals between franchise releases, not exclusively sequel waiting times. Films without membership records are described as unlisted rather than automatically classified as standalone.\n\n'
    text+=md(['Franchise','Recorded films','First release','Latest release','Span (days)'],spans)
    st=result['franchise_adjacent_gaps_days_stats']
    text+='\nAdjacent-release gaps within recorded franchises (days):\n\n'+md(['n','Min','Max','Mean','Median','Range','Sample SD','25%','75%'],[[st[k] for k in ['n','min','max','mean','median','range','sd','q1','q3']]])
    text+='\nUnlisted films: '+', '.join(result['films_without_franchise_records'])+'.\n'
    text+='\n**Use in Growing Up with Magic:** combine themes with release dates for an annotated movie–theme matrix; use franchise timelines to show how characters return across life stages. A reader-entered birth year could produce their age at each release, explicitly labeled as calculated age at release rather than age at first viewing. Neither dataset establishes that themes changed audience emotions or measures the same person over time. Before a full 31-film theme visualization, develop a coding rubric and fill coverage gaps through documented manual review.\n'
    text+='''
### 9. IMDb official data: documented prospective source

**Source / producer:** IMDb.com, Inc. **Accessed:** October 30, 2026. [IMDb Data](https://data.imdb.com/) describes licensed metadata products. The relevant public subset is documented separately under [IMDb Non-Commercial Datasets](https://data.imdb.com/non-commercial-datasets/), with files at [datasets.imdbws.com](https://datasets.imdbws.com/).

**Acquisition status:** documentation reviewed; official IMDb bulk files have **not** been downloaded or analyzed for this report. No official-file row counts, file sizes, descriptive statistics or validation findings are claimed. Existing IMDb scores in sections 4–5 came from the pinned pixarfilms CSV, not a direct IMDb bulk download. The [user-supplied Pixar list](https://www.imdb.com/list/ls087911008/) is a separate browsing reference; its membership has not been independently validated or imported.

| Candidate file | Documented columns | Intended project use |
| --- | --- | --- |
| title.basics.tsv.gz | 9: tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres | match film IDs and check titles, years, runtime and genre |
| title.ratings.tsv.gz | 3: tconst, averageRating, numVotes | obtain an explicitly dated rating and vote-count snapshot |
| title.crew.tsv.gz | 3: tconst, directors, writers | optional creator comparisons using person IDs |

**Format and structure:** gzipped UTF-8 TSV with a header; the backslash-N marker (`\\N`) denotes missing values. `tconst` is a title identifier/string and a potential join key. Title text and titleType are strings; years and runtime are nullable integers; isAdult is a boolean flag, not an MPA age rating; genres is a multi-value field. averageRating is numeric and numVotes is an integer. Directors and writers are arrays of person identifiers. These files cover broad IMDb title records, not an already filtered Disney/Pixar film collection. Select the project films using a verified catalogue and match by ID, title and year rather than assuming a genre or company-name filter identifies the correct population.

**Updates and limits:** IMDb states that the public files refresh daily. No particular snapshot timestamp has been acquired here. The documented public files do not include plot summaries, user-review text, viewer age groups, emotional themes or a Disney/Pixar studio-membership column. Those would require separately permitted sources or documented manual coding. Browsing an IMDb page is not equivalent to downloading a dataset.

**Terms and attribution:** this is copyrighted data under limited personal/non-commercial terms, not CC0 or unrestricted open data. See [IMDb non-commercial use guidance](https://help.imdb.com/article/imdb/general-information/can-i-use-imdb-data-in-my-software/G5JTRESSHJBBHTGX) and [Conditions of Use](https://www.imdb.com/conditions/). The guidance restricts republishing/recreating a movie database and automated website extraction, and requires the statement: “Information courtesy of IMDb (https://www.imdb.com). Used with permission.” These restrictions must be checked before using a future extract in a public repository or website. No IMDb bulk extract or review corpus is redistributed in this repository.

**Planned validation if acquired:** record download date, dimensions and checksums; test unique/nonmissing tconst keys, title/year matches, missing-value parsing, score ranges, nonnegative vote counts and unmatched project titles. Preserve a matching log and distinguish live IMDb ratings from the older pixarfilms snapshot. This is a future validation plan, not a claim that these checks have already been performed on IMDb bulk files.
'''
    return result,text
