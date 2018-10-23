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
        fields = {} if not (self.name) else {'name' : self.name}
        return fields
        
class AccountValues(DatabaseValues):
    '''
    account database object values representation
    '''
    def __init__(self, plan_id:int, joined_date:str, expiry_date:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'plan_id', plan_id)
        object.__setattr__(self, 'joined_date', joined_date)
        object.__setattr__(self, 'expiry_date', expiry_date)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all AccountValues fields
        '''
        fields = {'plan_id' : self.plan_id, 'joined_date' : self.joined_date, 'expiry_date' : self.expiry_date}
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
        :returns: a Account object constructed via the provided key
        :raises: None
        '''
        l = Account()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private instance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the provided key
        '''
        return Account.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Account object constructed from row
        '''
        name, plan_id, joined_date, expiry_date = row
        return Account(name, plan_id, joined_date, expiry_date)

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

    def __init__(self, name:str = None, plan_id:int = None, joined_date:str = None, expiry_date:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = AccountKeys(name)
        vals = AccountValues(plan_id, joined_date, expiry_date)

        super().__init__('account', keys, vals)

    def getTable(self):
        return self._table

    def getName(self):
        return self._keys.name
    
    
    def getPlan_Id(self):
        return self._vals.plan_id
    
    def getJoined_Date(self):
        return self._vals.joined_date
    
    def getExpiry_Date(self):
        return self._vals.expiry_date
    
    
    def setPlan_Id(self, plan_id:int):
       self._vals.plan_id = plan_id
    
    def setJoined_Date(self, joined_date:str):
       self._vals.joined_date = joined_date
    
    def setExpiry_Date(self, expiry_date:str):
       self._vals.expiry_date = expiry_date
    
    

    def isNullable(self, field):
        if field == 'expiry_date':
            return True
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
