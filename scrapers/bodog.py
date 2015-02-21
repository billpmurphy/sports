from app.sites import Site, Scraper
from app.utils import make_request, strip, TableParser
from data.data import nhl


def bodog_nhl_extractor(page):
    tp = TableParser()
    tp.feed(strip(page))
    tables = tp.get_tables()

    # Get rid of garbage rows
    rows = [r for t in tables for r in t if len(r) > 3][1:]

    # Find team names and moneylines
    pairs = []
    for i in range(len(rows)/2):
        name1 = rows[i*2][2].strip()
        name2 = rows[i*2+1][1].strip()
        moneyline1 = rows[i*2][4].strip()
        moneyline2 = rows[i*2+1][3].strip()
        pairs.append(((name1, moneyline1), (name2, moneyline2)))
    return pairs


bodog = Site("sports.bodog.eu", {})
bodog.scrapers[nhl] = Scraper(
    url="http://sports.bodog.eu/sports-betting/nhl-hockey-lines.jsp",
    fetch_fn=make_request,
    extract_fn=bodog_nhl_extractor)
