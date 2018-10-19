from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

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
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'date', date)
        object.__setattr__(self, 'league', league)
        object.__setattr__(self, 'home_team', home_team)
        object.__setattr__(self, 'away_team', away_team)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all MatchKeys fields
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
        '''
        object.__setattr__(self, 'result', result)
        object.__setattr__(self, 'best_odds', best_odds)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all MatchValues fields
        '''
        fields = None if not (self.result and self.best_odds) else {'result' : self.result, 'best_odds' : self.best_odds}
        return fields
        
class Match(DatabaseObject):
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
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private nstance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the primary key
        '''
        return Match.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Match object constructed from row
        '''
        date, league, home_team, away_team, result, best_odds = row
        return Match(date, league, home_team, away_team, result, best_odds)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Match object constructed from row
        '''
        return Match.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Match objects constructed from rows
        '''
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def _createMulti(cls, rows:tuple):
        '''
        Private instance method to create database objects from the provided 
        database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Match objects constructed from rows
        '''
        return Match.createMulti(rows)

    def __init__(self, date:str = None, league:str = None, home_team:str = None, away_team:str = None, result:str = None, best_odds:float = None):
        '''
        Construct the object from the provided table name, key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = MatchKeys(date, league, home_team, away_team)
        vals = MatchValues(result, best_odds)

        super().__init__('match', keys, vals)

    def getTable(self):
        return self._table

    def getDate(self):
        return self._keys.date
    
    def getLeague(self):
        return self._keys.league
    
    def getHome_Team(self):
        return self._keys.home_team
    
    def getAway_Team(self):
        return self._keys.away_team
    
    
    def getResult(self):
        return self._vals.result
    
    def getBest_Odds(self):
        return self._vals.best_odds
    
    
    def setResult(self, result:str):
       self._vals.result = result
    
    def setBest_Odds(self, best_odds:float):
       self._vals.best_odds = best_odds
    
    

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
