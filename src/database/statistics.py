from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

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
        
        fields = None if not (generation_date and algo_id and league) else {'generation_date' : generation_date, 'algo_id' : algo_id, 'league' : league}
        super().__init__('statistics', fields)

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
        
        fields = None if not (mark and mark_freq and home_freq and away_freq and draw_freq) else {'mark' : mark, 'mark_freq' : mark_freq, 'home_freq' : home_freq, 'away_freq' : away_freq, 'draw_freq' : draw_freq}
        super().__init__(fields)

class Statistics:
    '''
    statistics database object representation
    '''
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        '''
        Class method to create a database object with the provided primary key

        :param keys: a DatabaseKeys object
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
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
