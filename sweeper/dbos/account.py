from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class AccountKeys(DatabaseKeys):
    '''
    account database object primary key representation
    '''
    name:str = None
    

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
        fields = {} if None in (self.name,) else {'name' : self.name}
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
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Account object constructed via an AdhocKey of fields
        '''
        l = Account()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Account object constructed via an AdhocKey of fields
        '''
        return Account.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Account object constructed from row
        '''
        name, plan_id, joined_date, expiry_date = row
        return Account(name, plan_id, joined_date, expiry_date)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Account object constructed from row
        '''
        return Account.create(row)

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
