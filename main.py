import logging
import os
from datetime import datetime
from time import sleep

from sports import find_arb_pairs
from config import nhl
from config import bovada, mybookie
from config import ARCHIVE_PATH, LOG_PATH
from utils import archive


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

    # Scrape all the sites we know, check for arbs
    sports = [nhl]
    sites = [bovada, mybookie]

    while True:
        for sport in sports:
            wagers = []
            pages = [site.fetch_page_for_sport(sport) for site in sites]

            for (page, site) in zip(pages, sites):
                if page is not None:
                    scraped_wagers = site.extract_wagers_for_sport(sport, page)

                    if len(scraped_wagers) > 0:
                        archive(ARCHIVE_PATH, "%s_%s" %
                                (site.name, sport.sport_name),
                                scraped_wagers)
                        wagers += scraped_wagers
            arb_pairs = find_arb_pairs(wagers)
            logger.info("Arb pairs for %s: %s", sport.sport_name, arb_pairs)
        sleep(60 * 10)


if __name__ == "__main__":
    main()
