"""Extract factual film cards from official HTML and summarize the saved CSV.

One-time acquisition: python3 analysis/disney.py --from-html /path/to/films.html
Offline analysis: imported by analyze.py; Python standard library only.
"""
import csv, hashlib, json, re, sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT=Path(__file__).resolve().parents[1]
CSV=ROOT/'data/disney/disney_films.csv'
SOURCE='https://disneyanimation.com/films/'

class FilmParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.active=False; self.tag=None; self.buffer=''; self.card={}; self.rows=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='figure' and 'film' in attrs.get('class','').split():
            self.active=True; self.card={}
        if not self.active: return
        if tag in {'h4','p'}: self.tag=tag; self.buffer=''
        if tag=='a' and attrs.get('href','').startswith('/films/'):
            self.card['source_url']=urljoin(SOURCE,attrs['href'])
    def handle_data(self,data):
        if self.active and self.tag: self.buffer+=data
    def handle_endtag(self,tag):
        if not self.active: return
        if tag==self.tag:
            text=' '.join(self.buffer.split())
            if tag=='h4': self.card['film']=text
            if tag=='p' and re.fullmatch(r'\d{4}',text): self.card['release_year']=int(text)
            self.tag=None
        if tag=='figure':
            assert set(self.card)=={'film','release_year','source_url'},self.card
            self.rows.append(dict(self.card,studio='Walt Disney Animation Studios',access_date='2026-10-30'))
            self.active=False

def extract(path):
    raw=Path(path).read_bytes(); parser=FilmParser(); parser.feed(raw.decode('utf-8'))
    assert parser.rows,'No film cards found; inspect source structure.'
    CSV.parent.mkdir(parents=True,exist_ok=True)
    with CSV.open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['film','release_year','studio','source_url','access_date']); writer.writeheader(); writer.writerows(parser.rows)
    (ROOT/'sources/disney_acquisition.json').write_text(json.dumps({'source':SOURCE,'access_date':'2026-10-30','downloaded_html_bytes':len(raw),'downloaded_html_sha256':hashlib.sha256(raw).hexdigest(),'extraction':'figure elements with class film; h4 title, p year, /films/ link; upcoming promotional banner excluded','raw_html_redistributed':False},indent=2)+'\n')

def analyze(stats,md):
    rows=list(csv.DictReader(CSV.open(encoding='utf-8',newline='')))
    years=[int(r['release_year']) for r in rows]
    counts=Counter(years); decades=Counter(y//10*10 for y in years)
    dates=sorted(set(years)); gaps=[b-a for a,b in zip(sorted(years),sorted(years)[1:])]
    missing={k:sum(not r[k].strip() for r in rows) for k in rows[0]}
    result={'rows':len(rows),'columns':len(rows[0]),'bytes':CSV.stat().st_size,'sha256':hashlib.sha256(CSV.read_bytes()).hexdigest(),'missing':missing,'exact_duplicates':len(rows)-len({tuple(r.values()) for r in rows}),'duplicate_titles':len(rows)-len({r['film'] for r in rows}),'duplicate_source_urls':len(rows)-len({r['source_url'] for r in rows}),'release_year_stats':stats(years),'year_counts':dict(sorted(counts.items())),'decade_counts':dict(sorted(decades.items())),'interfilm_year_gap_stats':stats(gaps),'future_year_rows':sum(y>2026 for y in years),'source_order_descending':years==sorted(years,reverse=True)}
    assert not any(missing.values())
    assert not result['duplicate_source_urls']
    (ROOT/'analysis/disney_results.json').write_text(json.dumps(result,indent=2)+'\n')
    text='''
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

'''
    text+=f"**Actual size:** {len(rows)} rows × {len(rows[0])} columns; {CSV.stat().st_size:,} bytes. **Coverage:** {min(years)}–{max(years)}. Geography: studio film catalogue, not a regional audience dataset; the card years do not identify country-specific releases. The source page does not provide a reliable dataset update timestamp or fixed next update. Recheck when the studio releases films; access date must not be described as last update.\n\n"
    st=result['release_year_stats']
    text+='**Computed release-year statistics** (calendar year is a temporal coordinate; its mean is not average film age):\n\n'+md(['n','Min','Max','Mean','Median','Range','Sample SD','25%','75%'],[[st[k] for k in ['n','min','max','mean','median','range','sd','q1','q3']]])
    text+='\n**Films by decade:**\n\n'+md(['Decade','Films','Percent'],[[str(k)+'s',v,100*v/len(rows)] for k,v in sorted(decades.items())])
    text+='\n**Validation and remedies:**\n\n'+md(['Check','Actual finding'],[['Missing cells',sum(missing.values())],['Exact duplicate rows',result['exact_duplicates']],['Duplicate titles',result['duplicate_titles']],['Duplicate official URLs',result['duplicate_source_urls']],['Release years after 2026',result['future_year_rows']],['Source years descending',result['source_order_descending']]])
    text+='\nThe year field was required to match four digits during extraction. Chronological gaps are expected because the studio did not release a grid-listed film every year; they are not missing rows inferred by the analysis. Early and late dates are retained, not removed as outliers. Only years are available in this extract, so within-year order, exact release intervals and country-specific premieres remain unknown. Keep the catalogue title and URL when matching IMDb/Pixar tables and manually review title variants. There are no plot summaries, reviews, emotional labels or viewer ages in this dataset. The catalogue supports the Disney side of the project timeline; theme coding remains a separate task.\n'
    text+='''
**Rights:** the source displays Disney's all-rights-reserved copyright notice; no open-data licence was identified on the catalogue page. This project attributes Disney and publishes only a small factual title/year list and source links, not the copyrighted page design, images or descriptive prose. Do not label this extract CC0 or treat it as permission to reproduce Disney assets. Review [Disney terms](https://disneytermsofuse.com/) for any expanded reuse. The upstream Pixar package's CC0 licence does not apply to this new source.

**Reproduction:** the main analysis reads the saved CSV offline and regenerates its statistics and report. For a new acquisition, download the official page separately and run `python3 analysis/disney.py --from-html /path/to/films.html`. This refresh changes the snapshot and must be reviewed before replacing saved data.

### 11. Disney family-theme research: conceptual reference

Tanner, L. R., Haddock, S. A., Zimmerman, T. S., & Lund, L. K. (2003). *Images of Couples and Families in Disney Feature-Length Animated Films*. The American Journal of Family Therapy, 31(5), 355–373. [DOI and publisher page](https://doi.org/10.1080/01926180390223987). The journal issue year is 2003; the publisher separately lists an online publication date of March 22, 2012.

**Accessed:** October 30, 2026 (publisher abstract/metadata previously inspected, current direct automated access returned 403). The abstract describes analysis of 26 Disney animated films and identifies patterns concerning the importance of family, simplified family diversity, unequal parental portrayals and romantic relationship conventions. These ideas can inform a future coding rubric for family relationships; they are not a validated crosswalk to the Vox labels.

**Status:** literature reference only. Full text and original row-level coding data have not been acquired. The 26-film count is reported by the abstract, not independently computed here. No film-by-film labels, data dimensions, statistics or replication claims are inferred from it. Check the full methods and film sample through university library access before adapting its framework. The paper's earlier historical scope cannot establish patterns for newer films.

**Rights:** link and cite the paper; no open dataset licence was verified and no PDF, tables or coded dataset is redistributed. Any new annotations created for this project should have their own rubric, evidence, author and date, and be distinguished from the authors' findings.
'''
    return result,text

if __name__=='__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--from-html': extract(sys.argv[2])
    else: raise SystemExit(__doc__)
