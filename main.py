import logging
import os
from datetime import datetime
from time import sleep

from app.utils import archive_page, archive_pickle
from app.sports import find_arb_pairs
from data.data import nhl
from scrapers.betdsi import betdsi
from scrapers.bodog import bodog
from scrapers.bovada import bovada
from scrapers.mybookie import mybookie
from scrapers.sportsbook import sportsbook
from scrapers.sportsinteraction import sportsinteraction
from scrapers.topbet import topbet


ARCHIVE_PATH = "archive/"
LOG_PATH = "logs/"


def set_up():
    # Set up archiving, logging
    for file_path in [ARCHIVE_PATH, LOG_PATH]:
        if not os.path.exists(file_path):
            os.mkdir(file_path)

    logging.basicConfig(
        format="%(levelname)s,%(name)s,%(asctime)s,\"%(message)s\"",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
        filename="%slog_%s.log" %
                 (LOG_PATH, datetime.now().strftime("%Y-%m-%d_%H:%M:%S")))
    return


def main():
    set_up()
    logger = logging.getLogger(__name__)
    logger.info("Starting up.")

    wait_time = 60 * 10

    # Scrape all the sites we know, check for arbs
    sports = [nhl]
    sites = [bovada, mybookie, topbet, bodog, sportsinteraction, sportsbook,
             betdsi]

    while True:
        for sport in sports:
            pages = [site.fetch_page_for_sport(sport) for site in sites]
            site_pages = [(page, site) for (page, site) in zip(pages, sites)
                          if page is not None]

            wagers = []
            for (page, site) in site_pages:
                archive_page(ARCHIVE_PATH, "%s_%s_page" %
                             (site.name, sport.sport_name),
                             page)

                scraped_wagers = site.extract_wagers_for_sport(sport, page)
                print site, len(scraped_wagers)
                if len(scraped_wagers) > 0:
                    archive_pickle(ARCHIVE_PATH, "%s_%s_wagers" %
                                   (site.name, sport.sport_name),
                                   scraped_wagers)
                    wagers += scraped_wagers
            arb_pairs = find_arb_pairs(wagers)
            logger.info("Arb pairs for %s: %s", sport.sport_name, arb_pairs)
        logger.info("Sleeping for %s seconds.", wait_time)
        sleep(wait_time)
        print ""


if __name__ == "__main__":
    main()
