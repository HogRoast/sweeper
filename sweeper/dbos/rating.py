from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class RatingKeys(DatabaseKeys):
    '''
    rating database object primary key representation
    '''
    match_date:str = None
    league:str = None
    home_team:str = None
    away_team:str = None
    algo_id:int = None
    

    def __init__(self, match_date:str, league:str, home_team:str, away_team:str, algo_id:int):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'match_date', match_date)
        object.__setattr__(self, 'league', league)
        object.__setattr__(self, 'home_team', home_team)
        object.__setattr__(self, 'away_team', away_team)
        object.__setattr__(self, 'algo_id', algo_id)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all RatingKeys fields
        '''
        fields = {} if None in (self.match_date, self.league, self.home_team, self.away_team, self.algo_id,) else {'match_date' : self.match_date, 'league' : self.league, 'home_team' : self.home_team, 'away_team' : self.away_team, 'algo_id' : self.algo_id}
        return fields
        
class RatingValues(DatabaseValues):
    '''
    rating database object values representation
    '''
    def __init__(self, mark:int):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'mark', mark)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all RatingValues fields
        '''
        fields = {'mark' : self.mark}
        return fields
        
class Rating(DatabaseObject):
    '''
    rating database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Rating object constructed via an AdhocKey of fields
        '''
        l = Rating()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Rating object constructed via an AdhocKey of fields
        '''
        return Rating.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Rating object constructed from row
        '''
        match_date, league, home_team, away_team, algo_id, mark = row
        return Rating(match_date, league, home_team, away_team, algo_id, mark)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Rating object constructed from row
        '''
        return Rating.create(row)

    def __init__(self, match_date:str = None, league:str = None, home_team:str = None, away_team:str = None, algo_id:int = None, mark:int = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = RatingKeys(match_date, league, home_team, away_team, algo_id)
        vals = RatingValues(mark)

        super().__init__('rating', keys, vals)

    def getTable(self):
        return self._table

    def getMatch_Date(self):
        return self._keys.match_date
    
    def getLeague(self):
        return self._keys.league
    
    def getHome_Team(self):
        return self._keys.home_team
    
    def getAway_Team(self):
        return self._keys.away_team
    
    def getAlgo_Id(self):
        return self._keys.algo_id
    
    
    def getMark(self):
        return self._vals.mark
    
    
    def setMark(self, mark:int):
       self._vals.mark = mark
    
    

    def isNullable(self, field):
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
