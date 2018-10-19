from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues, AdhocKeys

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
        
        super().__init__('account_perms', self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all Account_permsKeys fields
        :raises: None
        '''
        fields = None if not (self.id) else {'id' : self.id}
        return fields
        
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
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all Account_permsValues fields
        :raises: None
        '''
        fields = None if not (self. account and self.league and self.algo_id) else {'account' : self.account, 'league' : self.league, 'algo_id' : self.algo_id}
        return fields
        
class Account_perms:
    '''
    account_perms database object representation
    '''
    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
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
        return self.keys.table + ' : Keys ' + str(self.keys.getFields()) + \
                ' : Values ' + str(self.vals.getFields())
