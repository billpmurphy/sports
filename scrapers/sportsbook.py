import re

from app.sites import Site, Scraper
from app.utils import make_request
from data.data import nhl


def sportsbook_nhl_extractor(page):
    page_stripped = re.sub("\t|\r\n|\n", "", page)
    teams = re.findall("<span class=\"team\" .+?>(.+?)</span>", page_stripped)
    moneylines = re.findall(" ate=\"ML[AH]\"><div class=\"market\">" +
                            "(.+?)</div></a>", page_stripped)

    if len(teams) != len(moneylines):
        return []

    pairs = [((teams[i*2], moneylines[i*2]), (teams[i*2+1], moneylines[i*2+1]))
             for i in range(len(teams)/2)]
    return pairs


sportsbook = Site("sportsbook.ag", {})
sportsbook.scrapers[nhl] = Scraper(
    url="https://www.sportsbook.ag/sbk/sportsbook4/" +
        "nhl-betting/nhl-game-lines.sbk",
    fetch_fn=make_request,
    extract_fn=sportsbook_nhl_extractor)
