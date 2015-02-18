import logging

from sports import Wager
from utils import strip, parse_moneyline, make_request, TableParser


logger = logging.getLogger(__name__)


class Scraper(object):
    """
    Represents a web page and a function for extracting the wagers from it.
    """
    def __init__(self, sport, site, url, extract_fn):
        self.sport = sport
        self.site = site
        self.url = url
        self.extract_fn = extract_fn

    def fetch_page(self):
        logger = logging.getLogger("Scraper %s %s" % (self.sport, self.site))
        logger.info("Fetching page. URL: %s", self.url)
        return make_request(self.url)

    def extract_wagers_from_page(self, page):
        logger = logging.getLogger("Scraper %s %s" % (self.sport, self.site))
        logger.info("Extracting wagers from page.")
        wagers = self.extract_fn(self.site, self.sport, page)
        logger.info("Extracted %s wagers from page.", len(wagers))
        return wagers


class SportNotFoundException(Exception):
    pass


class Site(object):
    """
    Represents a website, including a dictionary that maps Sport objects to
    functions that can scrape bets for that sport.
    """
    def __init__(self, name, scrapers):
        self.name = name
        self.scrapers = scrapers
        self.last_scrape_time = None

    def __repr__(self):
        return self.name

    def fetch_page_for_sport(self, sport):
        logger = logging.getLogger("Site %s" % self.name)
        logger.info("Requested fetch for %s", sport)
        if sport not in self.scrapers.keys():
            logger.warn("Sport %s not available to fetch.", sport)
            raise SportNotFoundException(sport)
        else:
            return self.scrapers[sport].fetch_page()

    def extract_wagers_for_sport(self, sport, page):
        logger = logging.getLogger("Site %s" % self.name)
        logger.info("Requested extract for %s", sport)
        if sport not in self.scrapers.keys():
            logger.warn("Sport %s not available to extract.", sport)
            raise SportNotFoundException(sport)
        else:
            return self.scrapers[sport].extract_wagers_from_page(page)


# Scraping/handling functions - hopefully there can be some reuse here

def collate_wagers(site, name_odds_pairs, sport):
    """
    Given pairs of ((team_name, odds), (team_name, odds)), parse the team names
    and collate the whole thing into a list of wagers.
    """
    wagers = []
    for (name1, moneyline1), (name2, moneyline2) in name_odds_pairs:
        team1 = sport.find_team_from_name(name1)
        team2 = sport.find_team_from_name(name2)
        odds1 = parse_moneyline(moneyline1)
        odds2 = parse_moneyline(moneyline2)

        if all(x is not None for x in (team1, team2, odds1, odds2)):
            wagers.append(Wager(site, team1, team2, odds1))
            wagers.append(Wager(site, team2, team1, odds2))
    return wagers


def bovada_nhl_scraper(site, sport, page):
    tp = TableParser()
    tp.feed(strip(page))
    tables = tp.get_tables()

    # Get rid of garbage lines in the table
    tables = tables[1:-1]
    for i, t in enumerate(tables):
        tables[i] = max(t, key=lambda x: len(x))

    # Find the team names and moneylines
    pairs = []
    for i in range(len(tables)/2):
        name1 = tables[i*2][2].strip()
        name2 = tables[i*2+1][1].strip()
        moneyline1 = tables[i*2][4].strip()
        moneyline2 = tables[i*2+1][3].strip()

        if moneyline1 is not None and moneyline2 is not None:
            pairs.append(((name1, moneyline1), (name2, moneyline2)))

    wagers = collate_wagers(site, pairs, sport)
    return wagers


def mybookie_nhl_scraper(site, sport, page):
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

    wagers = collate_wagers(site, pairs, sport)
    return wagers
