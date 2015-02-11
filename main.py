import logging
import os
from datetime import datetime

from sports import find_arb_pairs
from utils import archive
from config import nhl
from config import bovada, mybookie
from config import ARCHIVE_PATH, LOG_PATH


def main():
    logging.basicConfig(
        format="%(levelname)s,%(name)s,%(asctime)s,\"%(message)s\"",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
        filename="%stest_log %s.log" %
                 (LOG_PATH, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    logger = logging.getLogger(__name__)
    logger.info("Starting up.")

    for file_path in [ARCHIVE_PATH, LOG_PATH]:
        if not os.path.exists(file_path):
            os.mkdir(file_path)

    sports = [nhl]
    sites = [bovada, mybookie]

    for sport in sports:
        wagers = []
        for site in sites:
            scraped_wagers = site.scrape(sport)
            if len(scraped_wagers) > 0:
                archive(ARCHIVE_PATH, "%s %s" % (site.name, sport.sport_name),
                        scraped_wagers)
            wagers += scraped_wagers
        arb_pairs = find_arb_pairs(wagers)
        logger.info("Arb pairs for %s: %s", sport.sport_name, arb_pairs)


if __name__ == "__main__":
    main()
