from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class AlgoKeys(DatabaseKeys):
    id:int
    

    def __init__(self, id:int):
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'id', id)
        
        fields = None if not (id) else {'id' : id}
        super().__init__('algo', fields)

class AlgoValues(DatabaseValues):
    def __init__(self, name:str = None, desc:str = None):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'desc', desc)
        
        fields = None if not (name and desc) else {'name' : name, 'desc' : desc}
        super().__init__(fields)

class Algo:
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        l = Algo()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        id, name, desc = row
        return Algo(id, name, desc)

    @classmethod
    def createMulti(cls, rows:tuple):
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, id:int = None, name:str = None, desc:str = None):
        self.keys = AlgoKeys(id)
        self.vals = AlgoValues(name, desc)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
