import csv

from app.sports import Sport
from app.sports import Team


DATA_PATH = "data/"


def load_sport(sport_name, data_path):
    """
    Load team names and info from file, and return the list of teams.
    """
    with open("%s%s.csv" % (data_path, sport_name), "rb") as f:
        team_data = list(iter(csv.reader(f)))

    teams = [Team(*row[:3], other_names=row[3:]) for row in team_data]
    return Sport(sport_name, teams)


# Sports objects
nhl = load_sport("nhl", DATA_PATH)
#nba = load_sport("nba", DATA_PATH)
