from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class MatchKeys(DatabaseKeys):
    '''
    match database object primary key representation
    '''
    date:str
    league:str
    home_team:str
    away_team:str
    

    def __init__(self, date:str, league:str, home_team:str, away_team:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        :returns: N/A
        :raises: None
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'date', date)
        object.__setattr__(self, 'league', league)
        object.__setattr__(self, 'home_team', home_team)
        object.__setattr__(self, 'away_team', away_team)
        
        fields = None if not (date and league and home_team and away_team) else {'date' : date, 'league' : league, 'home_team' : home_team, 'away_team' : away_team}
        super().__init__('match', fields)

class MatchValues(DatabaseValues):
    '''
    match database object values representation
    '''
    def __init__(self, result:str = None, best_odds:float = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        :returns: N/A
        :raises: None
        '''
        object.__setattr__(self, 'result', result)
        object.__setattr__(self, 'best_odds', best_odds)
        
        fields = None if not (result and best_odds) else {'result' : result, 'best_odds' : best_odds}
        super().__init__(fields)

class Match:
    '''
    match database object representation
    '''
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        '''
        Class method to create a database object with the provided primary key

        :param keys: a DatabaseKeys object
        :returns: a Match object constructed via the primary key
        :raises: None
        '''
        l = Match()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Match object constructed from row
        :raises: None
        '''
        date, league, home_team, away_team, result, best_odds = row
        return Match(date, league, home_team, away_team, result, best_odds)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Match objects constructed from rows
        :raises: None
        '''
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, date:str = None, league:str = None, home_team:str = None, away_team:str = None, result:str = None, best_odds:float = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        self.keys = MatchKeys(date, league, home_team, away_team)
        self.vals = MatchValues(result, best_odds)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
