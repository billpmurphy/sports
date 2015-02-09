from collections import defaultdict


class Team(object):
    """
    Object to represent a team. For now, just the name and city and any
    alternate names, which we need when trying to parse web pages with team
    names and odds. If I ever do stat arb, some statistics will also go here.
    """
    def __init__(self, team_id, team_city, team_name, other_names=None):
        self.team_id = team_id
        self.team_city = team_city
        self.team_name = team_name
        self.other_names = other_names if other_names is not None else []

    def __eq__(self, other):
        return self.team_id == other.team_id

    def __repr__(self):
        return "<%s %s>" % (self.team_id, self.team_name)

    def __lt__(self, other):
        return self.team_id < other.team_id

    def matches_team_name(self, string):
        """
        See if an input string matches the team name, using various
        permutations of the name.
        """
        string = string.strip().lower()
        possible_matches = [name for name in self.other_names]
        possible_matches += [self.team_name, self.team_city,
                             self.team_city + " " + self.team_name]
        possible_matches = [s.lower() for s in possible_matches]
        return string in possible_matches


class Sport(object):
    """
    Object to represent a sport - for now, only the name and the list of teams.
    If I ever do stat arb, league statistics will also go here.
    """
    def __init__(self, sport_name, teams=None):
        self.sport_name = sport_name
        self.teams = teams if teams is not None else []

    def __repr__(self):
        return self.sport_name.upper()

    def find_team_from_name(self, string):
        """
        Given an input string, find the team that matches the string. If
        multiple teams or no teams match, return None.
        """
        matches = [t for t in self.teams if t.matches_team_name(string)]

        if len(matches) == 1:
            return matches[0]
        else:
            return None


class Wager(object):
    """
    Represent a wager, with functions for comparing wagers to see whether two
    wagers are betting on the same game, in the same direction or in the
    opposite direction.
    """
    def __init__(self, site, win_team, loss_team, odds):
        self.site = site
        self.win_team = win_team
        self.loss_team = loss_team
        self.odds = odds

    def __repr__(self):
        return "{%s:%s - 1:%s (%s)}" % \
            (self.win_team, self.loss_team, self.odds, self.site)

    def is_same(self, other):
        return self.win_team == other.win_team and \
            self.loss_team == other.loss_team

    def is_inverse(self, other):
        return self.win_team == other.loss_team and \
            self.loss_team == other.win_team


def hedge_ratio(wager1, wager2):
    """
    Given two wagers, find the optimal amount of capital
    to allocate to each bet in order to achieve the maximum possible return. If
    the two wagers are not actually opposing, return None.
    """
    if not wager1.is_inverse(wager2):
        return None
    c = (wager1.odds + 1.0) / (wager2.odds + 1.0)
    return (1.0/(c + 1.0), c/(c + 1.0))


def hedge_returns(wager1, wager2):
    """
    Calculate the returns from placing two wagers with the optimal hedge
    ratio.
    """
    hedge = hedge_ratio(wager1, wager2)
    if hedge is None:
        return 0

    wins1 = hedge[0] * (1 + wager1.odds)
    wins2 = hedge[1] * (1 + wager2.odds)
    return (wins1 + wins2) / 2.0


def find_arb_pairs(wager_list, returns=1.0):
    """
    Given a list of wagers, find any pairs of wagers that have arbitrage
    opportunities with returns above a certain threshold.
    """

    # Collate wagers by team
    wagers = defaultdict(lambda: [])
    for w in wager_list:
        wagers[(w.win_team, w.loss_team)].append(w)

    arb_pairs = []
    for team1, team2 in wagers.keys():
        # Avoid duplicate pairs, incomplete pairs
        if team1 > team2 or (team2, team1) not in wagers:
            continue

        # Find the most extreme bets for/against the two teams
        best_bet_on_team1 = max(wagers[(team1, team2)], key=lambda x: x.odds)
        best_bet_on_team2 = max(wagers[(team2, team1)], key=lambda x: x.odds)

        # If an optimal hedge here yields the desired returns, save the pair
        if hedge_returns(best_bet_on_team1, best_bet_on_team2) > returns:
            arb_pairs.append((best_bet_on_team1, best_bet_on_team2))

    return arb_pairs
