from app.sites import Site, Scraper
from app.utils import make_request, strip, TableParser
from data.data import nhl


def bovada_nhl_extractor(page):
    tp = TableParser()
    tp.feed(strip(page))
    tables = tp.get_tables()

    # Get rid of garbage lines in the table
    tables = tables[1:]
    for i, t in enumerate(tables):
        tables[i] = max(t, key=lambda x: len(x))

    # Find the team names and moneylines
    pairs = []
    for i in range(len(tables)/2):
        name1 = tables[i*2][2].strip()
        name2 = tables[i*2+1][1].strip()
        moneyline1 = tables[i*2][4].strip()
        moneyline2 = tables[i*2+1][3].strip()
        pairs.append(((name1, moneyline1), (name2, moneyline2)))
    return pairs


bovada = Site("bovada.lv", {})
bovada.scrapers[nhl] = Scraper(
    url="http://sports.bovada.lv/sports-betting/nhl-hockey-lines.jsp",
    fetch_fn=make_request,
    extract_fn=bovada_nhl_extractor)
