Getting this started.

TODO:
* More scraper functions for popular betting sites. This is a bit of a hassle
  but it's the main thing that needs to get done.
* Error handling (including good logging, responding well to failure, etc.) for
  critical pieces, mainly HTTP request sending.
* Better error handling for those annoying "cannot parse the thing" situations rather than
  returning/checking for None.
* More lists of teams for different sports, and alternate names for teams.
* Async requests for scrapers that just use `make_request`.



Eventual goal:
* Set up scrapers for multiple sports on as many betting sites as possible.
* Run the scraper for a while, logging and saving everything.
* Write some scripts to process the logs, looking for frequency of arbs,
  fluctuations in odds, etc, to see if this is actually feasible.


Notes on sites:

| Site                            | NHL | NBA | JS? | Notes |
| ------------------------------- | --- | --- | --- | |
|http://www.bovada.lv             |  x  |     |  no | |
|http://mybookie.ag               |  x  |     |  no | |
|http://topbet.eu/sportsbook      |  x  |     |  no | |
|http://sports.bodog.eu           |  x  |     |  no | |
|http://www.sportsinteraction.com |  x  |     |  no | |
|https://www.sportsbook.ag        |  x  |     |  no | |
|http://www.betdsi.eu             |  x  |     |  no | |
|http://www.sportsbetting.ag      |  x  |     | yes | selenium |
|http://www.pinnaclesports.com    |     |     |  no | has API |
|https://sports.bwin.com          |     |     |  no | |
|http://www.betonline.ag          |     |     | yes | |
|http://www.bookmaker.eu          |     |     | yes | |
|http://www.5dimes.eu             |     |     | yes | |
|http://www.sportsbettingonline.ag|     |     | yes | complex JS |
|http://www.wagerweb.ag           |     |     | yes | Login only |
|http://www.betus.com.pa          |     |     |  no | Login only |
|http://www.vietbet.eu            |     |     | yes | Login only |
|https://www.betfair.com          |     |     |  no | UK only |
