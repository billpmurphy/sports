from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from app.sites import Site, Scraper
from app.utils import TableParser
from data.data import nhl


def sportsbetting_nhl_fetcher(url):
    source = None
    driver = webdriver.Firefox()
    try:
        driver.get(url)

        # click on "Hockey" on sidebar
        driver.find_element_by_css_selector(
            "div.topNav:nth-child(15) > a:nth-child(1)").click()

        # click on "NHL" below that
        driver.find_element_by_css_selector(
            "div.subNav:nth-child(16) > div:nth-child(1) > a:nth-child(1)"
        ).click()

        # wait up to 10 seconds for DOM to be refreshed
        WebDriverWait(driver, 10).until(
            lambda _: "Hockey - NHL"
            in driver.page_source)

        source = driver.page_source
    finally:
        driver.close()
    return source


def sportsbetting_nhl_extractor(page):
    tp = TableParser()
    tp.feed(page)
    tables = tp.get_tables()

    # Clean up tables
    tables = tables[3][2:]
    tables = [r for r in tables if len(r) > 20]

    # Extract names/lines
    pairs = []
    for i in range(len(tables)/2):
        name1 = tables[i*2][2].strip()
        name2 = tables[i*2+1][1].strip()
        moneyline1 = str(tables[i*2][9]).strip()
        moneyline2 = str(tables[i*2+1][8]).strip()
        pairs.append(((name1, moneyline1), (name2, moneyline2)))
    return pairs


sportsbetting = Site("sportsbetting.ag", {})
sportsbetting.scrapers[nhl] = Scraper(
    url="http://www.sportsbetting.ag/sportsbook",
    fetch_fn=sportsbetting_nhl_fetcher,
    extract_fn=sportsbetting_nhl_extractor)
