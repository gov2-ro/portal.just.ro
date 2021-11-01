# portal.just.ro ⟶ sqlite

Descarcă arhiva via [portalquery.just.ro API](http://portal.just.ro/SitePages/acces.aspx) către un db sqlite

`fetchData(dateRange, instanta='all')`

instanta = 'all' | [slug_instanta1, slug_instanta2, ...]

if instanta='all' or None, loop all instanțe then fetch dosare & ședințe filtered by dateRange

### v0.1
- fetch api -> local xml
- local xml -> sqlite

### v0.2
- cron
- logging
- fetch api -> update sqlite
- check dupes?

