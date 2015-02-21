from app.sites import Site, Scraper
from app.utils import make_request, TableParser
from data.data import nhl


def topbet_nhl_extractor(page):
    tp = TableParser()
    tp.feed(page)
    tables = tp.get_tables()

    # Get rid of garbage tables
    tables = [t for t in tables if len(t) == 3 and t[0][0] == t[0][1] == 0]

    # Find team names and moneylines
    pairs = []
    for table in tables:
        name1 = table[1][1].strip()
        name2 = table[2][1].strip()
        moneyline1 = table[1][5].strip()
        moneyline2 = table[2][5].strip()
        pairs.append(((name1, moneyline1), (name2, moneyline2)))
    return pairs


topbet = Site("topbet.eu", {})
topbet.scrapers[nhl] = Scraper(
    url="http://topbet.eu/sportsbook/nhl",
    fetch_fn=make_request,
    extract_fn=topbet_nhl_extractor)
