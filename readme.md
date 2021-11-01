# portal.just.ro ⟶ sqlite

Descarcă arhiva via [portalquery.just.ro API](http://portal.just.ro/SitePages/acces.aspx) către un db sqlite

`fetchData(dateRange, instanta='all')`

instanta = 'all' | [slug_instanta1, slug_instanta2, ...]

if instanta='all' or None, loop all instanțe then fetch dosare & ședințe filtered by dateRange

## Commands
- `createDb.py <pato/to/db>` : creates sqlite db from config, if no path given
- `fetchAPI.py <date> <days=1> <direction=back>` : fetches date + days in direction [back|fwd] – fetches 24h after date
- `updateDb.py` : looks into xml folder, writes to db, moves to /parsed folder; also checks for dupes? – if dupe create log

## Roadmap

### v0.1
- [x] fetch api ⟶ local xml
- [x] local xml ⟶ sqlite prototype

### v0.2
- [x] prototype fetch ⟶ db sequence for 24h (1day)
- [ ] add relationships (Dosar)
  - [x] DosarParte
  - [ ] DosarSedinta
  - [ ] DosarCaleAtac

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