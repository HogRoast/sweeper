from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class LeagueKeys(DatabaseKeys):
    name: str

    def __init__(self, name:str):
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'name', name)
        fields = None if name is None else {'name' : name}
        super().__init__('league', fields)

class LeagueValues(DatabaseValues):
    def __init__(self, desc:str = None):
        self.desc = desc
        fields = None if desc is None else {'desc' : desc}
        super().__init__(fields)

class League:
    @classmethod
    def asAdhoc(cls, keys:DatabaseKeys):
        l = League()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        name, desc = row
        return League(name, desc)

    @classmethod
    def createMulti(cls, rows:tuple):
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, name:str = None, desc:str = None):
        self.keys = LeagueKeys(name)
        self.vals = LeagueValues(desc)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
