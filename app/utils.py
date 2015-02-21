import HTMLParser
import logging
import pickle
import re
from datetime import datetime
from urllib2 import Request, urlopen, URLError


logger = logging.getLogger(__name__)


# Web scraping utils

def make_request(url):
    """
    Send an HTTP request with the User-Agent set to the Firefox default, to
    make sure sites serve the page we want (and don't block us).
    If we cannot retrieve the page, log the error and return None.
    """
    logger = logging.getLogger("http_request")

    ff_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0)" + \
               "Gecko/20100101 Firefox/35.0"
    req = Request(url, headers={"User-Agent": ff_agent})

    logger.info("Sending request to %s", url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, "reason"):
            logger.error("Failed to reach a server. URL: %s Reason: %s",
                         (url, e.reason))
        elif hasattr(e, "code"):
            logger.error("The server couldn't fulfill the request. " +
                         "URL: %s Error code: %s", url, e.code)
        else:
            logger.error("Unknown URLError while making request. " +
                         "URL: %s Error: %s", url, str(e))
        return
    except Exception as e:
        logger.error("Unknown Exception while making request. " +
                     "URL: %s Exception: %s", url, str(e))
        return

    response_url = response.geturl()
    if response_url != url:
        logging.warn("Response url does not match requested url. " +
                     "Request: %s Response %s", url, response_url)

    try:
        page = response.read()
    except Exception as e:
        logger.error("Failed to read page from response. URL: %s Error: %s",
                     (url, str(e)))
        return

    logger.info("Successfully fetched page %s", url)
    return page


def strip(html_string):
    """
    Strip out unnecessary tags and characters from a web page, including
    Unicode, <p>, <span>, <div>, etc.
    """
    html_string = html_string.strip()
    html_string = re.sub("[^\x00-\x7F]", " ", html_string)
    html_string = re.sub("&nbsp;|\n|\r|\t|\r\n", " ", html_string)
    html_string = re.sub("<(p|span|div|a).+?>", " ", html_string)
    html_string = re.sub("</(p|span|div|a)>", " ", html_string)
    html_string = re.sub("<input.+?/>", " ", html_string)
    html_string = re.sub("\s{2,}", " ", html_string)
    html_string = html_string.encode("ascii", "ignore")
    return html_string


class TableParser(HTMLParser.HTMLParser):
    """
    Stack-based parser to extract HTML tables from a web page.
    Probably a good idea to use utils.strip() before feeding a page into the
    parser, otherwise <td>s containing <p>s, <span>s, etc, will not be parsed
    correctly.
    """
    def __init__(self):
        self.tp_reset()
        HTMLParser.HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.register = 0

    def handle_endtag(self, tag):
        if tag.lower() in ("td", "th"):
            self.curr_row.append(self.register)
        elif tag.lower() == "tr":
            self.curr_table.append(self.curr_row)
            self.curr_row = []
        elif tag.lower() == "table":
            self.tables.append(self.curr_table)
            self.curr_table = []

    def handle_data(self, data):
        self.register = data

    def get_tables(self):
        return self.tables

    def tp_reset(self):
        self.tables = []
        self.curr_table = []
        self.curr_row = []
        self.register = None


def parse_moneyline(string):
    """
    Attempt to parse a string containing a moneyline. If the string cannot be
    interpreted, return None.
    """
    if string.lower() in ["ev", "even", "100", "+100"]:
        return 1.0
    elif re.match("[+-][0-9]+?", string):
        line = float(string[1:])
        if string[0] == '+':
            return line/100.0
        else:
            return 100.0/line
    elif re.match("[0-9]+?", string):
        line = float(string)
        return line/100.0
    return


# Archiving/logging related utils

def archive_page(archive_path, filename, page):
    now = datetime.now().strftime("%Y-%M-%d_%H:%M:%S")
    archive_file = "%s%s_%s.html" % (archive_path, now, filename)
    logger.info("Archiving page in '%s'", archive_file)

    try:
        with open(archive_file, "wb") as f:
            f.write(page)
    except Exception as e:
        logger.error("Failed to archive page Error: %s", e)
    else:
        logger.info("Archive of page successful. Path: '%s'", archive_file)
    return


def archive_pickle(archive_path, filename, obj):
    now = datetime.now().strftime("%Y-%M-%d_%H:%M:%S")

    archive_file = "%s%s_%s.pickle" % (archive_path, now, filename)
    logger.info("Archiving objects in '%s'", archive_file)

    try:
        with open(archive_file, "wb") as f:
            pickle.dump(obj, f)
    except pickle.PickleError as e:
        logger.error("Cannot pickle object. Error %s", e)
    except Exception as e:
        logger.error("Failed to archive objects. Error: %s", e)
    else:
        logger.info("Archive of objects successful. Path: '%s'", archive_file)
    return
