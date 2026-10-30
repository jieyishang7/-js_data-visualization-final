"""Rebuild DATA_REPORT.md and results.json using Python 3 standard library only."""
import csv, json, math, statistics as s, hashlib
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
TABLES = {p.stem: list(csv.DictReader(p.open(encoding='utf-8', newline=''))) for p in sorted(RAW.glob('*.csv'))}
MISSING = {'', 'NA', 'N/A', 'null'}
def missing(x): return x in MISSING
def quantile(a, p):
    a=sorted(a); h=(len(a)-1)*p; i=int(h)
    return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(h-i)
def stats(a):
    n=len(a); mean=s.mean(a); sd=s.stdev(a); q1=quantile(a,.25); q3=quantile(a,.75)
    m2=s.mean([(v-mean)**2 for v in a]); m3=s.mean([(v-mean)**3 for v in a])
    return dict(n=n,min=min(a),max=max(a),mean=mean,median=s.median(a),range=max(a)-min(a),sd=sd,q1=q1,q3=q3,skew=m3/m2**1.5 if m2 else 0,lower=q1-1.5*(q3-q1),upper=q3+1.5*(q3-q1))
def md(headers, rows):
    def f(x): return f'{x:,.2f}' if isinstance(x,float) else str(x).replace('|','\\|').replace('\n',' ')
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(map(f,r))+' |' for r in rows])+'\n'
films=TABLES['pixar_films']; titles={r['film'] for r in films}
results={'dimensions':{},'missing':{},'duplicates':{},'joins':{},'numeric':{},'outliers':{}}
for name,rows in TABLES.items():
    results['dimensions'][name]={'rows':len(rows),'columns':len(rows[0]),'bytes':(RAW/(name+'.csv')).stat().st_size,'sha256':hashlib.sha256((RAW/(name+'.csv')).read_bytes()).hexdigest()}
    results['missing'][name]={k:sum(missing(r[k]) for r in rows) for k in rows[0]}
    keys=[tuple(r.values()) for r in rows]
    results['duplicates'][name]={'exact_rows':len(keys)-len(set(keys)),'duplicate_film_keys':len(rows)-len({r['film'] for r in rows}) if name not in {'genres','themes_vox'} else 'not applicable: multi-label table'}
    results['joins'][name]={'orphan_titles':sorted({r['film'] for r in rows}-titles),'films_without_rows':sorted(titles-{r['film'] for r in rows})}
numeric=[('pixar_films','run_time',1,'minutes'),('public_response','rotten_tomatoes_score',1,'0–100'),('public_response','metacritic_score',1,'0–100'),('public_response','imdb_score',1,'0–10'),('public_response','letterboxd_rating',1,'0–5'),('box_office','budget',1e6,'million USD'),('box_office','box_office_worldwide',1e6,'million USD')]
for name,col,scale,unit in numeric:
    pairs=[(r['film'],float(r[col])/scale) for r in TABLES[name] if not missing(r[col])]
    st=stats([v for _,v in pairs]); key=name+'.'+col; results['numeric'][key]=st
    results['outliers'][key]=[{'film':f,'value':v} for f,v in pairs if v<st['lower'] or v>st['upper']]
dates=sorted(date.fromisoformat(r['release_date']) for r in films)
years=Counter(d.year for d in dates); months=Counter(d.month for d in dates)
gaps=[(b-a).days for a,b in zip(dates,dates[1:])]
results['temporal']={'first':str(dates[0]),'last':str(dates[-1]),'year_counts':dict(sorted(years.items())),'month_counts':dict(sorted(months.items())),'gaps_days':stats(gaps),'zero_release_years':[y for y in range(dates[0].year,dates[-1].year+1) if y not in years],'future_rows':sum(d>date(2026,10,29) for d in dates)}
results['categories']={}
for name,col in [('pixar_films','film_rating'),('public_response','cinema_score'),('genres','category'),('genres','value')]:
    results['categories'][name+'.'+col]=dict(Counter(r[col] for r in TABLES[name] if not missing(r[col])).most_common())
reconciliation=[{'film':r['film'],'difference_usd':int(r['box_office_worldwide'])-int(r['box_office_us_canada'])-int(r['box_office_other'])} for r in TABLES['box_office'] if int(r['box_office_worldwide'])!=int(r['box_office_us_canada'])+int(r['box_office_other'])]
results['box_office_reconciliation']=reconciliation
results['truncated_plots']=[r['film'] for r in films if r['plot'].endswith('...')]
results['numeric_parse_errors']=[]; results['invalid_ranges']=[]
for name,rows in TABLES.items():
    for col in rows[0]:
        if col in {'film','film_rating','plot','release_date','category','value','cinema_score','theme','franchise'}: continue
        for r in rows:
            if missing(r[col]): continue
            try: v=float(r[col]); assert math.isfinite(v)
            except (ValueError,AssertionError): results['numeric_parse_errors'].append([name,r['film'],col]); continue
            limit=10 if col=='imdb_score' else 5 if col=='letterboxd_rating' else 100 if 'score' in col or col=='rotten_tomatoes_popcorn_meter_verified' else None
            if v<0 or (limit is not None and v>limit) or (col=='run_time' and v==0): results['invalid_ranges'].append([name,r['film'],col,v])
results['whitespace_cells']=sum(v!=v.strip() for rows in TABLES.values() for r in rows for v in r.values())
results['release_order_valid']=[int(r['number']) for r in films]==list(range(1,len(films)+1)) and [r['release_date'] for r in films]==sorted(r['release_date'] for r in films)
from supplement import analyze as analyze_supplement
supplement_results,supplement_report=analyze_supplement(TABLES,stats,md)
results['supplement']=supplement_results
(ROOT/'analysis/results.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n')
report='''# Growing Up with Magic: The Stories That Grow with Us

## Final Project Data Report

Columbia Data Visualization · Jieyi Shang · October 29, 2026

### Project question and scope

How can Pixar's films provide a timeline for exploring growing up, family, friendship, identity, and the stories people revisit at different stages of life? This acquisition report establishes a reproducible film-level foundation: release dates, runtime, rating, genres, reception, and financial context. It does **not** claim that review scores measure emotional impact, nostalgia, or how an individual changes with age. Those questions require separately documented audience research or transparent manual thematic coding. Disney data is excluded to keep definitions and provenance consistent.

### 1. Sources and acquisition

The primary source is Eric Leung's [pixarfilms](https://github.com/erictleung/pixarfilms), a community-maintained R data package, not an official Pixar dataset. Six linked CSV tables were downloaded on **October 29, 2026 (America/New_York)** by cloning the repository. Snapshot commit: [`e85a10a77b043d45fe8d950dbdf4d27886ccf520`](https://github.com/erictleung/pixarfilms/tree/e85a10a77b043d45fe8d950dbdf4d27886ccf520). Raw files here preserve the upstream bytes. The manifest in `analysis/results.json` records SHA-256 hashes and file sizes.

'''
descs={'pixar_films':('One film','Release order, release dates, runtime, MPA rating and brief plot. Wikipedia provides order/title/date; OMDb provides runtime/rating/plot.','2026-08-09'), 'public_response':('One film','Critic and audience reception from Rotten Tomatoes, Metacritic, CinemaScore, IMDb and Letterboxd, compiled in the package.','2026-08-09'), 'box_office':('One film','Budget and territorial/worldwide box-office gross in nominal USD, compiled from the package’s Wikipedia source.','2026-08-07'), 'genres':('One film–category–value assignment','Multiple genre and subgenre labels per film; upstream documentation identifies OMDb as source.','2026-08-07')}
rows=[]
for name,(grain,desc,updated) in descs.items():
    d=results['dimensions'][name]
    rows.append([f'[{name}](data/raw/{name}.csv)',d['rows'],d['columns'],d['bytes'],grain,updated])
report+=md(['Table / local download','Rows','Columns','Bytes','Row represents','Last file commit date'],rows)
report+='\nAll four tables were produced/compiled by Eric Leung and contributors. Individual table descriptions and immutable download links:\n\n'
for name,(_,desc,_) in descs.items(): report+=f'- **{name}:** {desc} [Original CSV](https://raw.githubusercontent.com/erictleung/pixarfilms/e85a10a77b043d45fe8d950dbdf4d27886ccf520/data-raw/{name}.csv).\n'
report+=f'''\nTotal download size is **{sum(d['bytes'] for d in results['dimensions'].values()):,} bytes** across six CSVs, readily manageable on a laptop. No credentials, API keys, or paid services are needed to analyze the saved snapshot.

**Coverage:** {dates[0]} through {dates[-1]}, {len(films)} films. This is a Pixar film collection, not a global sample of animation or a sample of viewers. MPA ratings are US classifications. Box office separates US/Canada and other territories, with worldwide totals. Reception websites aggregate their own users/critics and do not supply viewer geography or demographics here. Release dates follow the upstream list and should not be interpreted as every country's premiere date.

**Updates:** dates above are the most recent Git commits touching each CSV, not per-observation measurement timestamps. The repository's latest commit is August 20, 2026. The CSVs have no observation-level retrieval dates, and scores/grosses may lag the access date. No fixed next-update date is promised in the inspected documentation. Recheck upstream before the final visualization and preserve a new snapshot if refreshed. Upstream `.Rd` documentation is saved in `sources/`; its box-office dimensions are stale (24 rows), so this report uses actual CSV dimensions.

### 2. Schema and joining

CSV stores text; the following are analytical types. `NA` is parsed as missing, never zero. `film` is the exact title join key. Films, response and box office are one-to-one. Genres is one-to-many; aggregate genre membership before joining numerical measures to avoid multiplying a film's gross or score.

'''
schema=[['pixar_films','number','integer','release-order identifier, not a continuous measurement'],['pixar_films','film','string/key','film title'],['pixar_films','release_date','ISO date','upstream release date'],['pixar_films','run_time','integer','minutes'],['pixar_films','film_rating','categorical','MPA classification'],['pixar_films','plot','text','short synopsis; some are truncated'],['box_office','film','string/key','film title'],['box_office','budget; box_office_us_canada; box_office_other; box_office_worldwide','nullable integer','nominal USD; budget is production budget, not total costs'],['genres','film; category; value','strings / categorical','film and Genre/Subgenre label; multi-label'],['public_response','film','string/key','film title'],['public_response','rotten_tomatoes_score; metacritic_score; rotten_tomatoes_score_top_critics; rotten_tomatoes_popcorn_meter_score; rotten_tomatoes_popcorn_meter_verified','nullable numeric','scores on 0–100 scales; definitions differ across sites'],['public_response','imdb_score','decimal','0–10 observed scale; upstream Rd incorrectly says out of 100'],['public_response','letterboxd_rating','decimal','0–5 scale'],['public_response','cinema_score','nullable ordinal category','letter grade; do not average as a number'],['public_response','rotten_tomatoes_counts; metacritic_counts; imdb_counts; rotten_tomatoes_score_top_critics_votes; rotten_tomatoes_popcorn_meter_votes; rotten_tomatoes_popcorn_meter_verified_votes; letterboxd_counts; letterboxd_num_fans','nullable integer','review/vote/fan counts as supplied; rounded audience vote values may be thresholds rather than exact counts']]
report+=md(['Table','Columns','Analytical type','Meaning / unit'],schema)
report+='''
### 3. License and permitted use

The upstream repository includes [CC0 1.0 Universal](https://github.com/erictleung/pixarfilms/blob/e85a10a77b043d45fe8d950dbdf4d27886ccf520/LICENSE.md), preserved in [sources/PIXARFILMS-LICENSE.md](sources/PIXARFILMS-LICENSE.md). CC0 dedicates the contributor's applicable rights to the public domain to the extent possible, with a fallback license. It permits modification, redistribution and commercial use without an attribution condition. Academic attribution is nevertheless supplied here: **Eric Leung and contributors, pixarfilms, snapshot e85a10a, accessed October 29, 2026**.

CC0 does not clear third-party rights or trademarks. The package combines facts and text obtained from external sites; the upstream license does not establish that all source-site prose or media has been independently cleared. This project redistributes the package's small CSV snapshot under its stated license, keeps source credit, and uses numerical facts for analysis. It includes no film stills, posters, scripts or audio. Avoid reproducing plot text in a public visualization without reviewing its original terms. Relevant source documentation: [Wikipedia](https://en.wikipedia.org/wiki/List_of_Pixar_films), [OMDb](https://www.omdbapi.com/), and the archived upstream schema files in `sources/`. No fresh scraping of review platforms was performed.

### 4. Computed descriptive statistics

All following quantities are computed from the saved CSVs by [analysis/analyze.py](analysis/analyze.py), not copied from a description. Missing observations are omitted variable by variable; `n` shows the denominator. SD is sample standard deviation (n−1). Quantiles use linear interpolation at index (n−1)p. Skewness is the third population central moment divided by variance to the power 1.5. Values are rounded to two decimals only for display. Box-office and budget values below are in **millions of nominal US dollars**, without inflation adjustment.

'''
report+=md(['Variable (unit)','n','Min','Max','Mean','Median','Range','SD','25%','75%','Skewness'],[[col+' ('+unit+')']+[results['numeric'][name+'.'+col][k] for k in ['n','min','max','mean','median','range','sd','q1','q3','skew']] for name,col,_,unit in numeric])
report+='\n**Outliers:** values strictly outside Q1−1.5×IQR or Q3+1.5×IQR are flags for review, not automatic errors.\n\n'
report+=md(['Variable','Lower fence','Upper fence','Flagged films and values'],[[key,results['numeric'][key]['lower'],results['numeric'][key]['upper'],'; '.join(f"{r['film']}: {r['value']:.2f}" for r in vals) or 'None'] for key,vals in results['outliers'].items()])
report+='\nPositive skew means a longer upper tail; negative skew means a longer lower tail. Critic and audience scores are bounded and should be compared on their own scales. A negative score skew can reflect a concentration of highly rated films. Nominal revenue differences also reflect inflation, release strategy, and market conditions, not only popularity.\n\n**Categorical distributions**\n\n'
for key in ['pixar_films.film_rating','public_response.cinema_score','genres.category']:
    counts=results['categories'][key]; name,col=key.split('.'); total=len(TABLES[name]); report+=f'**{key}** (denominator {total} rows; missing shown separately):\n\n'+md(['Category','Count','Percent of all rows'],[[k,v,100*v/total] for k,v in counts.items()]+[['Missing',results['missing'][name][col],100*results['missing'][name][col]/total]])+'\n'
report+='**Genre/subgenre frequencies** (top 12 assignments; multi-label shares need not sum to 100%):\n\n'+md(['Label','Assignments','Percent of 31 films'],[[k,v,100*v/len(films)] for k,v in list(results['categories']['genres.value'].items())[:12]])
report+='\n**Temporal distribution**\n\n'+md(['Release year','Films'],sorted(years.items()))+'\n'+md(['Release month (1–12)','Films'],sorted(months.items()))
report+=f"\nThe inclusive period spans {dates[-1].year-dates[0].year+1} calendar years. Years with no recorded releases: {', '.join(map(str,results['temporal']['zero_release_years']))}. Adjacent-release gaps: min {min(gaps)} days, max {max(gaps)} days, mean {s.mean(gaps):.2f} days, median {s.median(gaps):.2f} days, sample SD {s.stdev(gaps):.2f} days. These are film-release events, not repeated measurements of the same audience. The final calendar year is partial as of the access date.\n"
report+='''
### 5. Actual validation findings and remedies

**Completeness:** each column was checked for blank, `NA`, `N/A`, or `null`. Only columns with missing values appear below; all omitted columns have zero missing cells.

'''
report+=md(['Table','Column','Missing','Percent','Affected films'],[[name,k,v,100*v/len(TABLES[name]),', '.join(r['film'] for r in TABLES[name] if missing(r[k]))] for name,cols in results['missing'].items() for k,v in cols.items() if v])
report+='\n**Duplicates and join coverage:**\n\n'+md(['Table','Exact duplicate rows','Duplicate film keys','Orphan titles','Films without rows'],[[name,d['exact_rows'],d['duplicate_film_keys'],len(results['joins'][name]['orphan_titles']),len(results['joins'][name]['films_without_rows'])] for name,d in results['duplicates'].items()])
report+=f"\n**Type, range, and temporal checks:** {len(results['numeric_parse_errors'])} numeric parsing errors; {len(results['invalid_ranges'])} negative/impossible numeric values under the documented scale checks; {results['whitespace_cells']} cells with leading/trailing whitespace; {results['temporal']['future_rows']} release dates after October 29, 2026. All release dates parsed as ISO dates. Sequential release numbers and chronological source order: {results['release_order_valid']}. These checks establish internal plausibility, not independent verification of every external fact.\n"
report+=f"\n**Financial reconciliation:** {len(reconciliation)} films have worldwide gross different from US/Canada plus other territories (exact integer-dollar check). Details: {json.dumps(reconciliation)}.\n"
report+=f"\n**Text anomalies:** {len(results['truncated_plots'])} synopses end in an ellipsis: {', '.join(results['truncated_plots'])}. These are incomplete inputs for thematic text analysis. No missing text was invented.\n"
report+='''
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
'''
report+=supplement_report
(ROOT/'DATA_REPORT.md').write_text(report,encoding='utf-8')
print(json.dumps({'dimensions':results['dimensions'],'missing':{n:{k:v for k,v in c.items() if v} for n,c in results['missing'].items()},'outliers':results['outliers'],'reconciliation':reconciliation},indent=2))
