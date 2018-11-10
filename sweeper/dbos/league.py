from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class LeagueKeys(DatabaseKeys):
    '''
    league database object primary key representation
    '''
    mnemonic:str
    

    def __init__(self, mnemonic:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'mnemonic', mnemonic)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all LeagueKeys fields
        '''
        fields = {} if not (self.mnemonic) else {'mnemonic' : self.mnemonic}
        return fields
        
class LeagueValues(DatabaseValues):
    '''
    league database object values representation
    '''
    def __init__(self, name:str, desc:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'desc', desc)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all LeagueValues fields
        '''
        fields = {'name' : self.name, 'desc' : self.desc}
        return fields
        
class League(DatabaseObject):
    '''
    league database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: League object constructed via an AdhocKey of fields
        '''
        l = League()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: League object constructed via an AdhocKey of fields
        '''
        return League.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a League object constructed from row
        '''
        mnemonic, name, desc = row
        return League(mnemonic, name, desc)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a League object constructed from row
        '''
        return League.create(row)

    def __init__(self, mnemonic:str = None, name:str = None, desc:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = LeagueKeys(mnemonic)
        vals = LeagueValues(name, desc)

        super().__init__('league', keys, vals)

    def getTable(self):
        return self._table

    def getMnemonic(self):
        return self._keys.mnemonic
    
    
    def getName(self):
        return self._vals.name
    
    def getDesc(self):
        return self._vals.desc
    
    
    def setName(self, name:str):
       self._vals.name = name
    
    def setDesc(self, desc:str):
       self._vals.desc = desc
    
    

    def isNullable(self, field):
        if field == 'desc':
            return True
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
