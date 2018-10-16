from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class TeamKeys(DatabaseKeys):
    name:str
    

    def __init__(self, name:str):
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'name', name)
        
        fields = None if not (name) else {'name' : name}
        super().__init__('team', fields)

class TeamValues(DatabaseValues):
    def __init__(self, league:str = None):
        object.__setattr__(self, 'league', league)
        
        fields = None if not (league) else {'league' : league}
        super().__init__(fields)

class Team:
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        l = Team()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        name, league = row
        return Team(name, league)

    @classmethod
    def createMulti(cls, rows:tuple):
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, name:str = None, league:str = None):
        self.keys = TeamKeys(name)
        self.vals = TeamValues(league)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
