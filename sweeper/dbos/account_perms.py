from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class Account_PermsKeys(DatabaseKeys):
    '''
    account_perms database object primary key representation
    '''
    id:int = None
    

    def __init__(self, id:int):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'id', id)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all Account_PermsKeys fields
        '''
        fields = {} if None in (self.id,) else {'id' : self.id}
        return fields
        
class Account_PermsValues(DatabaseValues):
    '''
    account_perms database object values representation
    '''
    def __init__(self, account:str, league:str, algo_id:int):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'account', account)
        object.__setattr__(self, 'league', league)
        object.__setattr__(self, 'algo_id', algo_id)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all Account_PermsValues fields
        '''
        fields = {'account' : self.account, 'league' : self.league, 'algo_id' : self.algo_id}
        return fields
        
class Account_Perms(DatabaseObject):
    '''
    account_perms database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Account_Perms object constructed via an AdhocKey of fields
        '''
        l = Account_Perms()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Account_Perms object constructed via an AdhocKey of fields
        '''
        return Account_Perms.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Account_Perms object constructed from row
        '''
        id, account, league, algo_id = row
        return Account_Perms(id, account, league, algo_id)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Account_Perms object constructed from row
        '''
        return Account_Perms.create(row)

    def __init__(self, id:int = None, account:str = None, league:str = None, algo_id:int = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = Account_PermsKeys(id)
        vals = Account_PermsValues(account, league, algo_id)

        super().__init__('account_perms', keys, vals)

    def getTable(self):
        return self._table

    def getId(self):
        return self._keys.id
    
    
    def getAccount(self):
        return self._vals.account
    
    def getLeague(self):
        return self._vals.league
    
    def getAlgo_Id(self):
        return self._vals.algo_id
    
    
    def setAccount(self, account:str):
       self._vals.account = account
    
    def setLeague(self, league:str):
       self._vals.league = league
    
    def setAlgo_Id(self, algo_id:int):
       self._vals.algo_id = algo_id
    
    

    def isNullable(self, field):
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
