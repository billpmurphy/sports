from app.sites import Site, Scraper
from app.utils import make_request, strip, TableParser
from data.data import nhl


def betdsi_nhl_extractor(page):
    tp = TableParser()
    tp.feed(strip(page))
    tables = tp.get_tables()

    # Get rid of garbage rows
    tables = [t for t in tables if len(t) == 2]

    # Find team names and moneylines
    pairs = []
    for table in tables:
        name1 = table[0][1].strip()
        name2 = table[1][0]
        moneyline1 = table[0][-1].strip()
        moneyline2 = table[1][-1].strip()
        pairs.append(((name1, moneyline1), (name2, moneyline2)))
    return pairs


betdsi = Site("betdsi.eu", {})
betdsi.scrapers[nhl] = Scraper(
    url="http://www.betdsi.eu/hockey-betting",
    fetch_fn=make_request,
    extract_fn=betdsi_nhl_extractor)
