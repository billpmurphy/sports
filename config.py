import csv

from scrapers import Site, Scraper
from scrapers import bovada_nhl_scraper, mybookie_nhl_scraper
from sports import Sport, Team


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

mybookie = Site("mybookie", {})
mybookie.scrapers[nhl] = Scraper(nhl, mybookie,
    "http://mybookie.ag/sportsbook/nhl-betting-lines/",
    mybookie_nhl_scraper)
