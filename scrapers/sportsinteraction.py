import re

from app.sites import Site, Scraper
from app.utils import make_request
from data.data import nhl


def sportsinteraction_nhl_extractor(page):
    # pull rows with regular moneylines out of page
    page_stripped = re.sub("\t|\r\n|\n", "", page)
    row_pattern = "<span class=\"name\">(.+?)</span>" + \
                  "<span class=\"handicap\">(.+?)</span>" + \
                  "<span class=\"price\">(.+?)</span>"
    rows = re.findall(row_pattern, page_stripped)
    moneyline_rows = [(r[0], r[2]) for r in rows if r[1].strip() == "&nbsp;"]

    # Find team names and moneylines
    pairs = []
    for i in range(len(moneyline_rows)/2):
        name1 = moneyline_rows[i*2][0].strip()
        name2 = moneyline_rows[i*2+1][0].strip()
        moneyline1 = moneyline_rows[i*2][1].strip()
        moneyline2 = moneyline_rows[i*2+1][1].strip()
        pairs.append(((name1, moneyline1), (name2, moneyline2)))
    return pairs


sportsinteraction = Site("sportsinteraction.com", {})
sportsinteraction.scrapers[nhl] = Scraper(
        url="http://www.sportsinteraction.com/hockey/nhl-betting-lines/",
        fetch_fn=make_request,
        extract_fn=sportsinteraction_nhl_extractor)
