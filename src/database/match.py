from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues, AdhocKeys

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
        
        super().__init__('match', self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all MatchKeys fields
        :raises: None
        '''
        fields = None if not (self.date and self.league and self.home_team and self.away_team) else {'date' : self.date, 'league' : self.league, 'home_team' : self.home_team, 'away_team' : self.away_team}
        return fields
        
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
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all MatchValues fields
        :raises: None
        '''
        fields = None if not (self. result and self.best_odds) else {'result' : self.result, 'best_odds' : self.best_odds}
        return fields
        
class Match:
    '''
    match database object representation
    '''
    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
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
        return self.keys.table + ' : Keys ' + str(self.keys.getFields()) + \
                ' : Values ' + str(self.vals.getFields())
