from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues, AdhocKeys

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
        
        super().__init__('account', self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all AccountKeys fields
        :raises: None
        '''
        fields = None if not (self.name) else {'name' : self.name}
        return fields
        
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
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all AccountValues fields
        :raises: None
        '''
        fields = None if not (self. expiry_date and self.joined_date and self.plan_id) else {'expiry_date' : self.expiry_date, 'joined_date' : self.joined_date, 'plan_id' : self.plan_id}
        return fields
        
class Account:
    '''
    account database object representation
    '''
    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
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
        return self.keys.table + ' : Keys ' + str(self.keys.getFields()) + \
                ' : Values ' + str(self.vals.getFields())
