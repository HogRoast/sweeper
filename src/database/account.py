from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class AccountKeys(DatabaseKeys):
    '''
    account database object primary key representation
    '''
    name:str
    

    def __init__(self, name:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        :returns: N/A
        :raises: None
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'name', name)
        
        fields = None if not (name) else {'name' : name}
        super().__init__('account', fields)

class AccountValues(DatabaseValues):
    '''
    account database object values representation
    '''
    def __init__(self, expiry_date:str = None, joined_date:str = None, plan_id:int = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        :returns: N/A
        :raises: None
        '''
        object.__setattr__(self, 'expiry_date', expiry_date)
        object.__setattr__(self, 'joined_date', joined_date)
        object.__setattr__(self, 'plan_id', plan_id)
        
        fields = None if not (expiry_date and joined_date and plan_id) else {'expiry_date' : expiry_date, 'joined_date' : joined_date, 'plan_id' : plan_id}
        super().__init__(fields)

class Account:
    '''
    account database object representation
    '''
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        '''
        Class method to create a database object with the provided primary key

        :param keys: a DatabaseKeys object
        :returns: a Account object constructed via the primary key
        :raises: None
        '''
        l = Account()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Account object constructed from row
        :raises: None
        '''
        name, expiry_date, joined_date, plan_id = row
        return Account(name, expiry_date, joined_date, plan_id)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Account objects constructed from rows
        :raises: None
        '''
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, name:str = None, expiry_date:str = None, joined_date:str = None, plan_id:int = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        self.keys = AccountKeys(name)
        self.vals = AccountValues(expiry_date, joined_date, plan_id)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
