from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class AccountKeys(DatabaseKeys):
    name:str
    

    def __init__(self, name:str):
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'name', name)
        
        fields = None if not (name) else {'name' : name}
        super().__init__('account', fields)

class AccountValues(DatabaseValues):
    def __init__(self, expiry_date:str = None, joined_date:str = None, plan_id:int = None):
        object.__setattr__(self, 'expiry_date', expiry_date)
        object.__setattr__(self, 'joined_date', joined_date)
        object.__setattr__(self, 'plan_id', plan_id)
        
        fields = None if not (expiry_date and joined_date and plan_id) else {'expiry_date' : expiry_date, 'joined_date' : joined_date, 'plan_id' : plan_id}
        super().__init__(fields)

class Account:
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        l = Account()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        name, expiry_date, joined_date, plan_id = row
        return Account(name, expiry_date, joined_date, plan_id)

    @classmethod
    def createMulti(cls, rows:tuple):
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, name:str = None, expiry_date:str = None, joined_date:str = None, plan_id:int = None):
        self.keys = AccountKeys(name)
        self.vals = AccountValues(expiry_date, joined_date, plan_id)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
