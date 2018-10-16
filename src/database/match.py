from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class MatchKeys(DatabaseKeys):
    date:str
    league:str
    home_team:str
    away_team:str
    

    def __init__(self, date:str, league:str, home_team:str, away_team:str):
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'date', date)
        object.__setattr__(self, 'league', league)
        object.__setattr__(self, 'home_team', home_team)
        object.__setattr__(self, 'away_team', away_team)
        
        fields = None if not (date and league and home_team and away_team) else {'date' : date, 'league' : league, 'home_team' : home_team, 'away_team' : away_team}
        super().__init__('match', fields)

class MatchValues(DatabaseValues):
    def __init__(self, result:str = None, best_odds:float = None):
        object.__setattr__(self, 'result', result)
        object.__setattr__(self, 'best_odds', best_odds)
        
        fields = None if not (result and best_odds) else {'result' : result, 'best_odds' : best_odds}
        super().__init__(fields)

class Match:
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        l = Match()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        date, league, home_team, away_team, result, best_odds = row
        return Match(date, league, home_team, away_team, result, best_odds)

    @classmethod
    def createMulti(cls, rows:tuple):
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, date:str = None, league:str = None, home_team:str = None, away_team:str = None, result:str = None, best_odds:float = None):
        self.keys = MatchKeys(date, league, home_team, away_team)
        self.vals = MatchValues(result, best_odds)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
