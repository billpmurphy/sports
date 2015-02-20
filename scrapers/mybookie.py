from app.sites import Site, Scraper
from app.utils import make_request, TableParser
from data.data import nhl


def mybookie_nhl_extractor(page):
    tp = TableParser()
    tp.feed(page)
    tables = tp.get_tables()

    # Get rid of garbage lines in the table
    tables = tables[0][1:]

    # Find team names and moneylines
    pairs = []
    for i in range(len(tables)/2):
        name1 = tables[i*2][2].strip().split(" ")[-1]
        name2 = tables[i*2+1][1].strip().split(" ")[-1]
        moneyline1 = str(tables[i*2][-1]).strip()
        moneyline2 = str(tables[i*2+1][-1]).strip()

        if moneyline1 is not None and moneyline2 is not None:
            pairs.append(((name1, moneyline1), (name2, moneyline2)))
    return pairs


mybookie = Site("mybookie.ag", {})
mybookie.scrapers[nhl] = Scraper(
        url="http://mybookie.ag/sportsbook/nhl-betting-lines/",
        fetch_fn=make_request,
        extract_fn=mybookie_nhl_extractor)
