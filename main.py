import logging
import os
from datetime import datetime
from time import sleep

from sports import find_arb_pairs
from config import nhl
from config import bovada, mybookie, topbet, bodog, sportsinteraction
from config import ARCHIVE_PATH, LOG_PATH
from utils import archive_page, archive_pickle


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
    sites = [bovada, mybookie, topbet, bodog, sportsinteraction]

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

                if len(scraped_wagers) > 0:
                    archive_pickle(ARCHIVE_PATH, "%s_%s_wagers" %
                                   (site.name, sport.sport_name),
                                   scraped_wagers)
                    wagers += scraped_wagers
            arb_pairs = find_arb_pairs(wagers)
            logger.info("Arb pairs for %s: %s", sport.sport_name, arb_pairs)
        logger.info("Sleeping for %s seconds.", wait_time)
        sleep(wait_time)


if __name__ == "__main__":
    main()
