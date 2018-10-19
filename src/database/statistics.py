from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues, AdhocKeys

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
        :returns: N/A
        :raises: None
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'generation_date', generation_date)
        object.__setattr__(self, 'algo_id', algo_id)
        object.__setattr__(self, 'league', league)
        
        super().__init__('statistics', self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all StatisticsKeys fields
        :raises: None
        '''
        fields = None if not (self.generation_date and self.algo_id and self.league) else {'generation_date' : self.generation_date, 'algo_id' : self.algo_id, 'league' : self.league}
        return fields
        
class StatisticsValues(DatabaseValues):
    '''
    statistics database object values representation
    '''
    def __init__(self, mark:int = None, mark_freq:int = None, home_freq:int = None, away_freq:int = None, draw_freq:int = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        :returns: N/A
        :raises: None
        '''
        object.__setattr__(self, 'mark', mark)
        object.__setattr__(self, 'mark_freq', mark_freq)
        object.__setattr__(self, 'home_freq', home_freq)
        object.__setattr__(self, 'away_freq', away_freq)
        object.__setattr__(self, 'draw_freq', draw_freq)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all StatisticsValues fields
        :raises: None
        '''
        fields = None if not (self. mark and self.mark_freq and self.home_freq and self.away_freq and self.draw_freq) else {'mark' : self.mark, 'mark_freq' : self.mark_freq, 'home_freq' : self.home_freq, 'away_freq' : self.away_freq, 'draw_freq' : self.draw_freq}
        return fields
        
class Statistics:
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
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Statistics object constructed from row
        :raises: None
        '''
        generation_date, algo_id, league, mark, mark_freq, home_freq, away_freq, draw_freq = row
        return Statistics(generation_date, algo_id, league, mark, mark_freq, home_freq, away_freq, draw_freq)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Statistics objects constructed from rows
        :raises: None
        '''
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, generation_date:str = None, algo_id:int = None, league:str = None, mark:int = None, mark_freq:int = None, home_freq:int = None, away_freq:int = None, draw_freq:int = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        self.keys = StatisticsKeys(generation_date, algo_id, league)
        self.vals = StatisticsValues(mark, mark_freq, home_freq, away_freq, draw_freq)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.getFields()) + \
                ' : Values ' + str(self.vals.getFields())
