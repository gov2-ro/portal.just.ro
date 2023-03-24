# portal.just.ro ⟶ sqlite

Descarcă arhiva via [portalquery.just.ro API](http://portal.just.ro/SitePages/acces.aspx) către un db sqlite

`fetchData(dateRange, instanta='all')`

instanta = 'all' | [slug_instanta1, slug_instanta2, ...]

if instanta='all' or None, loop all instanțe then fetch dosare & ședințe filtered by dateRange

## Commands
- `createDb.py <pato/to/db>` : creates sqlite db from config, if no path given
- `fetchAPI.py <date> <days=1> <direction=back>` : fetches date + days in direction [back|fwd] – fetches 24h after date
- `updateDb.py` : looks into xml folder, writes to db, moves to /parsed folder; also checks for dupes? – if dupe create log


## SQL db schema + Prompts

Given the following SQLite Database containing data about lawsuits archive with the following tables schema:

- "trials" (id: TEXT, data: DATE, court: TEXT, category: TEXT, status: TEXT)
- "parties" (trial_id: TEXT, name: TEXT, type: TEXT)
- "appeals" (trial_id: TEXT, date: DATE, appealing_party: TEXT, type: TEXT)
- "courts"  (name: TEXT, id: TEXT, county: TEXT, type: TEXT, parent: TEXT)

Where we have the following relationships:

- trial_id in parties and appeals tabbles is linked to the trials.id
- courts.parent is the parent of the court, which is a value from courts.id
- trials.court is one of the values from courts.id





# Roadmap

## Stats / SQL

- [ ] SQL stats - via GPT
  - [x] describe db schema

- [x] n-grams 

## UI

## Fetching

### v0.1
- [x] fetch api ⟶ local xml
- [x] local xml ⟶ sqlite prototype

### v0.2
- [x] prototype fetch ⟶ db sequence for 24h (1day)
- [x] add relationships (Dosar)
  - [x] DosarParte
  - [x] DosarSedinta
  - [x] DosarCaleAtac

#### v0.25
- [ ] sedinte
  - [ ] Sedinta
  - [ ] SedintaDosar

### v0.3 
- [ ] commands w arguments
- [ ] logging
- [ ] fetch api ⟶ update sqlite

### v0.4
- [ ] check for fetch errors
- [ ] check dupes?
- [ ] cron

#### v0.45
- [ ] Datasette template + dashboards

### v0.5
- [ ] nosql db