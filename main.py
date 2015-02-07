import logging
import os
from datetime import datetime

from sports import find_arb_pairs
from utils import archive
from config import nhl
from config import bovada
from config import ARCHIVE_PATH


def main():
    logging.basicConfig(
        format="%(levelname)s,%(name)s,%(asctime)s,\"%(message)s\"",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,
        filename="test_log %s.log" %
                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    logging.info("Starting up.")

    if not os.path.exists(ARCHIVE_PATH):
        os.mkdir(ARCHIVE_PATH)

    sports = [nhl]
    sites = [bovada]

    for sport in sports:
        wagers = []
        for site in sites:
            scraped_wagers = site.scrape(sport)
            if len(scraped_wagers) > 0:
                archive(ARCHIVE_PATH, "%s %s" % (site.name, sport.sport_name),
                        scraped_wagers)
            wagers += scraped_wagers
        arb_pairs = find_arb_pairs(wagers)
        logging.info("Arb pairs for %s: %s", sport.sport_name, arb_pairs)


if __name__ == "__main__":
    main()
