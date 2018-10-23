from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class StatisticsKeys(DatabaseKeys):
    '''
    statistics database object primary key representation
    '''
    generation_date:str
    algo_id:int
    league:str
    

    def __init__(self, generation_date:str, algo_id:int, league:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'generation_date', generation_date)
        object.__setattr__(self, 'algo_id', algo_id)
        object.__setattr__(self, 'league', league)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all StatisticsKeys fields
        '''
        fields = {} if not (self.generation_date and self.algo_id and self.league) else {'generation_date' : self.generation_date, 'algo_id' : self.algo_id, 'league' : self.league}
        return fields
        
class StatisticsValues(DatabaseValues):
    '''
    statistics database object values representation
    '''
    def __init__(self, mark:int = None, mark_freq:int = None, home_freq:int = None, away_freq:int = None, draw_freq:int = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'mark', mark)
        object.__setattr__(self, 'mark_freq', mark_freq)
        object.__setattr__(self, 'home_freq', home_freq)
        object.__setattr__(self, 'away_freq', away_freq)
        object.__setattr__(self, 'draw_freq', draw_freq)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the non-None value fields for this object in a dictionary form
        
        :returns: a dictionary of all StatisticsValues fields
        '''
        fields = {'mark' : self.mark, 'mark_freq' : self.mark_freq, 'home_freq' : self.home_freq, 'away_freq' : self.away_freq, 'draw_freq' : self.draw_freq}
        fields = dict([(k, v) for (k, v) in fields.items() if v is not None])
        return fields
        
class Statistics(DatabaseObject):
    '''
    statistics database object representation
    '''

    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
        :returns: a Statistics object constructed via the primary key
        :raises: None
        '''
        l = Statistics()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private nstance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the primary key
        '''
        return Statistics.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Statistics object constructed from row
        '''
        generation_date, algo_id, league, mark, mark_freq, home_freq, away_freq, draw_freq = row
        return Statistics(generation_date, algo_id, league, mark, mark_freq, home_freq, away_freq, draw_freq)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Statistics object constructed from row
        '''
        return Statistics.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Statistics objects constructed from rows
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
        :returns: a list of Statistics objects constructed from rows
        '''
        return Statistics.createMulti(rows)

    def __init__(self, generation_date:str = None, algo_id:int = None, league:str = None, mark:int = None, mark_freq:int = None, home_freq:int = None, away_freq:int = None, draw_freq:int = None):
        '''
        Construct the object from the provided table name, key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = StatisticsKeys(generation_date, algo_id, league)
        vals = StatisticsValues(mark, mark_freq, home_freq, away_freq, draw_freq)

        super().__init__('statistics', keys, vals)

    def getTable(self):
        return self._table

    def getGeneration_Date(self):
        return self._keys.generation_date
    
    def getAlgo_Id(self):
        return self._keys.algo_id
    
    def getLeague(self):
        return self._keys.league
    
    
    def getMark(self):
        return self._vals.mark
    
    def getMark_Freq(self):
        return self._vals.mark_freq
    
    def getHome_Freq(self):
        return self._vals.home_freq
    
    def getAway_Freq(self):
        return self._vals.away_freq
    
    def getDraw_Freq(self):
        return self._vals.draw_freq
    
    
    def setMark(self, mark:int):
       self._vals.mark = mark
    
    def setMark_Freq(self, mark_freq:int):
       self._vals.mark_freq = mark_freq
    
    def setHome_Freq(self, home_freq:int):
       self._vals.home_freq = home_freq
    
    def setAway_Freq(self, away_freq:int):
       self._vals.away_freq = away_freq
    
    def setDraw_Freq(self, draw_freq:int):
       self._vals.draw_freq = draw_freq
    
    

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
