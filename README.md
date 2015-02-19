Getting this started.

TODO:
* More scraper functions for popular betting sites. This is a bit of a hassle
  but it's the main thing that needs to get done.
* ~~Refactor the relationship between Sites, scraper functions, and Sports. There
  is a weird data dependency, because we need to know which functions are for
  which sports at compile-time and we also need the list of teams at runtime so
  that the scraper can parse the team names. Possibly also move some stuff to utils.py.~~
* ~~Error handling (including good logging, responding well to failure, etc.) for
  critical pieces, mainly HTTP request sending.~~
* Better error handling for those annoying "cannot parse the thing" situations rather than
  returning/checking for None.
* Is there some better way of setting up Sports/Site objects than config.py?
  Some kind of factory pattern?
* More lists of teams for different sports, and alternate names for teams.
* ~~Improve the logger, let each function set up its own logger instance, and add
  a custom logger that starts a new log every day.~~



Eventual goal:
* Set up scrapers for multiple sports on as many betting sites as possible.
* Run the scraper for a while, logging and saving everything.
* Write some scripts to process the logs, looking for frequency of arbs,
  fluctuations in odds, etc, to see if this is actually feasible.


Notes on sites:

| Site | Notes |
| ---- | ----- |
|http://www.bovada.lv/ | Have NHL scraper |
|http://mybookie.ag | Have NHL scraper |
|http://topbet.eu/sportsbook | Have NHL scraper |
|http://sports.bodog.eu | Have NHL scraper |
|http://www.sportsinteraction.com | Have NHL scraper |
|https://www.sportsbook.ag | No JS, should be doable |
|http://www.pinnaclesports.com/ | No JS, should be doable |
|https://sports.bwin.com | No JS, should be doable |
|http://www.betus.com.pa | No JS, should be doable |
|http://www.sportsbetting.ag | Uses JS to load |
|http://www.betonline.ag | Uses JS to load |
|http://www.bookmaker.eu/sportsbook.aspx | Uses JS to load |
|http://www.wagerweb.ag | Uses JS to load |
|http://www.betdsi.eu | Uses JS to load |
|http://www.5dimes.eu | Uses JS to load |
|http://www.sportsbettingonline.ag | Uses JS to load |
|http://www.vietbet.eu | Login required |
