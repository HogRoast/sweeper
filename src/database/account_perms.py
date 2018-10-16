from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class Account_permsKeys(DatabaseKeys):
    id:int
    

    def __init__(self, id:int):
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'id', id)
        
        fields = None if not (id) else {'id' : id}
        super().__init__('account_perms', fields)

class Account_permsValues(DatabaseValues):
    def __init__(self, account:str = None, league:str = None, algo_id:int = None):
        object.__setattr__(self, 'account', account)
        object.__setattr__(self, 'league', league)
        object.__setattr__(self, 'algo_id', algo_id)
        
        fields = None if not (account and league and algo_id) else {'account' : account, 'league' : league, 'algo_id' : algo_id}
        super().__init__(fields)

class Account_perms:
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        l = Account_perms()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        id, account, league, algo_id = row
        return Account_perms(id, account, league, algo_id)

    @classmethod
    def createMulti(cls, rows:tuple):
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, id:int = None, account:str = None, league:str = None, algo_id:int = None):
        self.keys = Account_permsKeys(id)
        self.vals = Account_permsValues(account, league, algo_id)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
