from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class PlanKeys(DatabaseKeys):
    id:int
    

    def __init__(self, id:int):
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'id', id)
        
        fields = None if not (id) else {'id' : id}
        super().__init__('plan', fields)

class PlanValues(DatabaseValues):
    def __init__(self, name:str = None, desc:str = None, cost:float = None):
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'desc', desc)
        object.__setattr__(self, 'cost', cost)
        
        fields = None if not (name and desc and cost) else {'name' : name, 'desc' : desc, 'cost' : cost}
        super().__init__(fields)

class Plan:
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        l = Plan()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        id, name, desc, cost = row
        return Plan(id, name, desc, cost)

    @classmethod
    def createMulti(cls, rows:tuple):
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, id:int = None, name:str = None, desc:str = None, cost:float = None):
        self.keys = PlanKeys(id)
        self.vals = PlanValues(name, desc, cost)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
