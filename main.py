import logging
import os
from datetime import datetime

from sports import find_arb_pairs
from utils import archive
from config import nhl
from config import bovada, mybookie
from config import ARCHIVE_PATH, LOG_PATH


def main():
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
    logger = logging.getLogger(__name__)
    logger.info("Starting up.")

    # Scrape all the sites we know, check for arbs
    sports = [nhl]
    sites = [bovada, mybookie]

    for sport in sports:
        wagers = []
        for site in sites:
            if sport in site.scrapers:
                page = site.fetch_page_for_sport(sport)

                if page is not None:
                    scraped_wagers = site.extract_wagers_for_sport(sport, page)

                    if len(scraped_wagers) > 0:
                        archive(ARCHIVE_PATH,
                                "%s_%s" % (site.name, sport.sport_name),
                                scraped_wagers)
                        wagers += scraped_wagers
        arb_pairs = find_arb_pairs(wagers)
        logger.info("Arb pairs for %s: %s", sport.sport_name, arb_pairs)


if __name__ == "__main__":
    main()
