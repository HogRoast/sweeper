from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class StatisticsKeys(DatabaseKeys):
    generation_date:str
    algo_id:int
    league:str
    

    def __init__(self, generation_date:str, algo_id:int, league:str):
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'generation_date', generation_date)
        object.__setattr__(self, 'algo_id', algo_id)
        object.__setattr__(self, 'league', league)
        
        fields = None if not (generation_date and algo_id and league) else {'generation_date' : generation_date, 'algo_id' : algo_id, 'league' : league}
        super().__init__('statistics', fields)

class StatisticsValues(DatabaseValues):
    def __init__(self, mark:int = None, mark_freq:int = None, home_freq:int = None, away_freq:int = None, draw_freq:int = None):
        object.__setattr__(self, 'mark', mark)
        object.__setattr__(self, 'mark_freq', mark_freq)
        object.__setattr__(self, 'home_freq', home_freq)
        object.__setattr__(self, 'away_freq', away_freq)
        object.__setattr__(self, 'draw_freq', draw_freq)
        
        fields = None if not (mark and mark_freq and home_freq and away_freq and draw_freq) else {'mark' : mark, 'mark_freq' : mark_freq, 'home_freq' : home_freq, 'away_freq' : away_freq, 'draw_freq' : draw_freq}
        super().__init__(fields)

class Statistics:
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        l = Statistics()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        generation_date, algo_id, league, mark, mark_freq, home_freq, away_freq, draw_freq = row
        return Statistics(generation_date, algo_id, league, mark, mark_freq, home_freq, away_freq, draw_freq)

    @classmethod
    def createMulti(cls, rows:tuple):
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, generation_date:str = None, algo_id:int = None, league:str = None, mark:int = None, mark_freq:int = None, home_freq:int = None, away_freq:int = None, draw_freq:int = None):
        self.keys = StatisticsKeys(generation_date, algo_id, league)
        self.vals = StatisticsValues(mark, mark_freq, home_freq, away_freq, draw_freq)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
