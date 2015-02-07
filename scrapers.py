import logging
from datetime import datetime

from sports import Wager
from utils import fetch_tables, parse_moneyline


class Site(object):
    """
    Represents a website, including a dictionary that maps Sport objects to
    functions that can scrape bets for that sport.
    """
    def __init__(self, name, scraper_fn_dict):
        self.name = name
        self.scraper_fn_dict = scraper_fn_dict
        self.last_scrape_time = None

    def __repr__(self):
        return self.name

    def scrape(self, sport):
        logging.info("Requested scrape for (%s;%s).",
                     self.name, sport)
        if sport in self.scraper_fn_dict:
            wagers = self.scraper_fn_dict[sport](self, sport)

            logging.info("Scrape (%s;%s) finished: %s wagers found.",
                         self.name, sport, len(wagers))
            self.last_scrape_time = datetime.now()
            return wagers
        else:
            logging.info("Scraper for (%s;%s) unavailable; skipping",
                         self.name, sport)
            return []


# Scraping/handling functions - hopefully there can be some reuse here

def collate_wagers(site, name_odds_pairs, sport):
    """
    Given pairs of ((team_name, odds), (team_name, odds)), parse the team names
    and collate the whole thing into a list of wagers.
    """
    wagers = []
    for (name1, odds1), (name2, odds2) in name_odds_pairs:
        team1 = sport.find_team_from_name(name1)
        team2 = sport.find_team_from_name(name2)

        if team1 is not None and team2 is not None:
            wagers.append(Wager(site, team1, team2, odds1))
            wagers.append(Wager(site, team2, team1, odds2))
    return wagers


def bovada_nhl_scraper(site, sport):
    url = "http://sports.bovada.lv/sports-betting/nhl-hockey-lines.jsp"
    tables = fetch_tables(url)

    # Get rid of garbage lines in the table
    tables = tables[1:-1]
    for i, t in enumerate(tables):
        tables[i] = max(t, key=lambda x: len(x))

    # Find the team names and moneylines
    pairs = []
    for i in range(len(tables)/2):
        name1 = tables[i*2][2].strip()
        moneyline1 = parse_moneyline(tables[i*2][4].strip())
        name2 = tables[i*2+1][1].strip()
        moneyline2 = parse_moneyline(tables[i*2+1][3].strip())

        if moneyline1 is not None and moneyline2 is not None:
            pairs.append(((name1, moneyline1), (name2, moneyline2)))
    return collate_wagers(site, pairs, sport)
