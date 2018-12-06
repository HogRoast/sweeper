from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class MatchKeys(DatabaseKeys):
    '''
    match database object primary key representation
    '''
    date:str = None
    league:str = None
    home_team:str = None
    away_team:str = None
    

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
        fields = {} if None in (self.date, self.league, self.home_team, self.away_team,) else {'date' : self.date, 'league' : self.league, 'home_team' : self.home_team, 'away_team' : self.away_team}
        return fields
        
class MatchValues(DatabaseValues):
    '''
    match database object values representation
    '''
    def __init__(self, result:str = None, best_odds_h:float = None, best_odds_d:float = None, best_odds_a:float = None, home_goals:int = None, away_goals:int = None, home_lp:int = None, away_lp:int = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'result', result)
        object.__setattr__(self, 'best_odds_h', best_odds_h)
        object.__setattr__(self, 'best_odds_d', best_odds_d)
        object.__setattr__(self, 'best_odds_a', best_odds_a)
        object.__setattr__(self, 'home_goals', home_goals)
        object.__setattr__(self, 'away_goals', away_goals)
        object.__setattr__(self, 'home_lp', home_lp)
        object.__setattr__(self, 'away_lp', away_lp)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all MatchValues fields
        '''
        fields = {'result' : self.result, 'best_odds_h' : self.best_odds_h, 'best_odds_d' : self.best_odds_d, 'best_odds_a' : self.best_odds_a, 'home_goals' : self.home_goals, 'away_goals' : self.away_goals, 'home_lp' : self.home_lp, 'away_lp' : self.away_lp}
        return fields
        
class Match(DatabaseObject):
    '''
    match database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Match object constructed via an AdhocKey of fields
        '''
        l = Match()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Match object constructed via an AdhocKey of fields
        '''
        return Match.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Match object constructed from row
        '''
        date, league, home_team, away_team, result, best_odds_h, best_odds_d, best_odds_a, home_goals, away_goals, home_lp, away_lp = row
        return Match(date, league, home_team, away_team, result, best_odds_h, best_odds_d, best_odds_a, home_goals, away_goals, home_lp, away_lp)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Match object constructed from row
        '''
        return Match.create(row)

    def __init__(self, date:str = None, league:str = None, home_team:str = None, away_team:str = None, result:str = None, best_odds_h:float = None, best_odds_d:float = None, best_odds_a:float = None, home_goals:int = None, away_goals:int = None, home_lp:int = None, away_lp:int = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = MatchKeys(date, league, home_team, away_team)
        vals = MatchValues(result, best_odds_h, best_odds_d, best_odds_a, home_goals, away_goals, home_lp, away_lp)

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
    
    def getBest_Odds_H(self):
        return self._vals.best_odds_h
    
    def getBest_Odds_D(self):
        return self._vals.best_odds_d
    
    def getBest_Odds_A(self):
        return self._vals.best_odds_a
    
    def getHome_Goals(self):
        return self._vals.home_goals
    
    def getAway_Goals(self):
        return self._vals.away_goals
    
    def getHome_Lp(self):
        return self._vals.home_lp
    
    def getAway_Lp(self):
        return self._vals.away_lp
    
    
    def setResult(self, result:str):
       self._vals.result = result
    
    def setBest_Odds_H(self, best_odds_h:float):
       self._vals.best_odds_h = best_odds_h
    
    def setBest_Odds_D(self, best_odds_d:float):
       self._vals.best_odds_d = best_odds_d
    
    def setBest_Odds_A(self, best_odds_a:float):
       self._vals.best_odds_a = best_odds_a
    
    def setHome_Goals(self, home_goals:int):
       self._vals.home_goals = home_goals
    
    def setAway_Goals(self, away_goals:int):
       self._vals.away_goals = away_goals
    
    def setHome_Lp(self, home_lp:int):
       self._vals.home_lp = home_lp
    
    def setAway_Lp(self, away_lp:int):
       self._vals.away_lp = away_lp
    
    

    def isNullable(self, field):
        if field == 'result':
            return True
        elif field == 'best_odds_h':
            return True
        elif field == 'best_odds_d':
            return True
        elif field == 'best_odds_a':
            return True
        elif field == 'home_goals':
            return True
        elif field == 'away_goals':
            return True
        elif field == 'home_lp':
            return True
        elif field == 'away_lp':
            return True
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
