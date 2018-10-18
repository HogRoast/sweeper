from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class Account_permsKeys(DatabaseKeys):
    '''
    account_perms database object primary key representation
    '''
    id:int
    

    def __init__(self, id:int):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        :returns: N/A
        :raises: None
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'id', id)
        
        fields = None if not (id) else {'id' : id}
        super().__init__('account_perms', fields)

class Account_permsValues(DatabaseValues):
    '''
    account_perms database object values representation
    '''
    def __init__(self, account:str = None, league:str = None, algo_id:int = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        :returns: N/A
        :raises: None
        '''
        object.__setattr__(self, 'account', account)
        object.__setattr__(self, 'league', league)
        object.__setattr__(self, 'algo_id', algo_id)
        
        fields = None if not (account and league and algo_id) else {'account' : account, 'league' : league, 'algo_id' : algo_id}
        super().__init__(fields)

class Account_perms:
    '''
    account_perms database object representation
    '''
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        '''
        Class method to create a database object with the provided primary key

        :param keys: a DatabaseKeys object
        :returns: a Account_perms object constructed via the primary key
        :raises: None
        '''
        l = Account_perms()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Account_perms object constructed from row
        :raises: None
        '''
        id, account, league, algo_id = row
        return Account_perms(id, account, league, algo_id)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Account_perms objects constructed from rows
        :raises: None
        '''
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, id:int = None, account:str = None, league:str = None, algo_id:int = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        self.keys = Account_permsKeys(id)
        self.vals = Account_permsValues(account, league, algo_id)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
