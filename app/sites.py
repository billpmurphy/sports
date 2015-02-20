import logging
import re

from sports import Wager
from utils import strip, parse_moneyline, make_request, TableParser


logger = logging.getLogger(__name__)


class Scraper(object):
    """
    Represents a web page and a function for extracting the wagers from it.
    """
    def __init__(self, url, fetch_fn, extract_fn):
        self.url = url
        self.fetch_fn = fetch_fn
        self.extract_fn = extract_fn

    def fetch_page(self):
        logger = logging.getLogger("Scraper [%s]" % self.url)
        logger.info("Fetching page.")
        try:
            page = self.fetch_fn(self.url)
        except Exception as e:
            logger.error("Exception in fetch fn. %s: %s", str(e), e.message)
            return None
        logger.info("Fetch successful.")
        return page

    def extract_wager_pairs_from_page(self, page):
        logger = logging.getLogger("Scraper [%s]" % self.url)

        if page is None:
            logger.error("No page to extract wagers from.")
            return []

        logger.info("Extracting wagers from page.")
        try:
            wagers = self.extract_fn(page)
        except Exception as e:
            logger.error("Exception in extraction fn. %s: %s",
                         str(e), e.message)
            return []
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
            wagers = self.scrapers[sport].extract_wager_pairs_from_page(page)
            return collate_wagers(self, wagers, sport)


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
