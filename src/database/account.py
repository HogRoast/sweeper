from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

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
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'name', name)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all AccountKeys fields
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
        '''
        object.__setattr__(self, 'expiry_date', expiry_date)
        object.__setattr__(self, 'joined_date', joined_date)
        object.__setattr__(self, 'plan_id', plan_id)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all AccountValues fields
        '''
        fields = None if not (self.expiry_date and self.joined_date and self.plan_id) else {'expiry_date' : self.expiry_date, 'joined_date' : self.joined_date, 'plan_id' : self.plan_id}
        return fields
        
class Account(DatabaseObject):
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
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private nstance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the primary key
        '''
        return Account.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Account object constructed from row
        '''
        name, expiry_date, joined_date, plan_id = row
        return Account(name, expiry_date, joined_date, plan_id)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Account object constructed from row
        '''
        return Account.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Account objects constructed from rows
        '''
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def _createMulti(cls, rows:tuple):
        '''
        Private instance method to create database objects from the provided 
        database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Account objects constructed from rows
        '''
        return Account.createMulti(rows)

    def __init__(self, name:str = None, expiry_date:str = None, joined_date:str = None, plan_id:int = None):
        '''
        Construct the object from the provided table name, key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = AccountKeys(name)
        vals = AccountValues(expiry_date, joined_date, plan_id)

        super().__init__('account', keys, vals)

    def getTable(self):
        return self._table

    def getName(self):
        return self._keys.name
    
    
    def getExpiry_Date(self):
        return self._vals.expiry_date
    
    def getJoined_Date(self):
        return self._vals.joined_date
    
    def getPlan_Id(self):
        return self._vals.plan_id
    
    
    def setExpiry_Date(self, expiry_date:str):
       self._vals.expiry_date = expiry_date
    
    def setJoined_Date(self, joined_date:str):
       self._vals.joined_date = joined_date
    
    def setPlan_Id(self, plan_id:int):
       self._vals.plan_id = plan_id
    
    

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
