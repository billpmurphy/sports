import HTMLParser
import logging
import pickle
import re
import urllib2
from datetime import datetime


# Web scraping utils

def make_request(url):
    """
    Send an HTTP request with the User-Agent set to the Firefox default, to
    make sure sites serve the page we want (and don't block us).
    """
    req = urllib2.Request(url,
                          headers={"User-Agent":
                                   "Mozilla/5.0 (Windows NT 6.1; WOW64; " +
                                   "rv:31.0 Gecko/20100101 Firefox/31.0"})
    logging.info("Sending request to %s", url)
    page = urllib2.urlopen(req).read()
    logging.info("Fetched page %s", url)
    return page


def strip(html_string):
    """
    Strip out unnecessary tags and characters from a web page, including
    Unicode, <p>, <span>, <div>, etc.
    """
    html_string = html_string.strip()
    html_string = re.sub("[^\x00-\x7F]", " ", html_string)
    html_string = re.sub("\n|\r|\t", " ", html_string)
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


def fetch_tables(url):
    """
    Fetch a page from a URL, strip it, grab the tables.
    """
    page = strip(make_request(url))
    tp = TableParser()
    tp.feed(strip(page))
    return tp.get_tables()


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
    return


# Archiving/logging related utils

def archive(archive_path, filename,  obj):
    now = datetime.now().strftime("%Y-%M-%d %H:%M:%S")
    archive_file = "%s%s %s.pickle" % (archive_path, now, filename)
    with open(archive_file, "wb") as f:
        pickle.dump(obj, f)
    logging.info("Archiving objects in '%s'", archive_file)
    return
