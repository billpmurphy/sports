import csv

from sports import Sport, Team
from scrapers import Site, Scraper
from scrapers import bovada_nhl_scraper
from scrapers import mybookie_nhl_scraper
from scrapers import topbet_nhl_scraper
from scrapers import bodog_nhl_scraper
from scrapers import sportsinteraction_nhl_scraper

DATA_PATH = "data/"
ARCHIVE_PATH = "archive/"
LOG_PATH = "logs/"


def load_teams(sport_name, data_path):
    """
    Load team names and info from file, and return the list of teams.
    """
    with open("%s%s.csv" % (data_path, sport_name), "rb") as f:
        team_data = list(iter(csv.reader(f)))

    teams = []
    for row in team_data:
        teams.append(Team(*row[:3], other_names=row[3:]))
    return teams


# Sports objects
nhl = Sport("nhl", teams=load_teams("nhl", data_path=DATA_PATH))


# Site objects
bovada = Site("bovada.lv", {})
bovada.scrapers[nhl] = Scraper(nhl, bovada,
        "http://sports.bovada.lv/sports-betting/nhl-hockey-lines.jsp",
        bovada_nhl_scraper)

mybookie = Site("mybookie.ag", {})
mybookie.scrapers[nhl] = Scraper(nhl, mybookie,
    "http://mybookie.ag/sportsbook/nhl-betting-lines/",
    mybookie_nhl_scraper)

topbet = Site("topbet.eu", {})
topbet.scrapers[nhl] = Scraper(nhl, topbet,
    "http://topbet.eu/sportsbook/nhl",
    topbet_nhl_scraper)

bodog = Site("sports.bodog.eu", {})
bodog.scrapers[nhl] = Scraper(nhl, bodog,
    "http://sports.bodog.eu/sports-betting/nhl-hockey-lines.jsp",
    bodog_nhl_scraper)

sportsinteraction = Site("sportsinteraction.com", {})
sportsinteraction.scrapers[nhl] = Scraper(nhl, sportsinteraction,
    "http://www.sportsinteraction.com/hockey/nhl-betting-lines/",
    sportsinteraction_nhl_scraper)
