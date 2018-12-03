from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class SourceKeys(DatabaseKeys):
    '''
    source database object primary key representation
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
        
        :returns: a dictionary of all SourceKeys fields
        '''
        fields = {} if None in (self.id,) else {'id' : self.id}
        return fields
        
class SourceValues(DatabaseValues):
    '''
    source database object values representation
    '''
    def __init__(self, name:str, fixtures_url:str, url:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'fixtures_url', fixtures_url)
        object.__setattr__(self, 'url', url)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all SourceValues fields
        '''
        fields = {'name' : self.name, 'fixtures_url' : self.fixtures_url, 'url' : self.url}
        return fields
        
class Source(DatabaseObject):
    '''
    source database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Source object constructed via an AdhocKey of fields
        '''
        l = Source()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Source object constructed via an AdhocKey of fields
        '''
        return Source.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Source object constructed from row
        '''
        id, name, fixtures_url, url = row
        return Source(id, name, fixtures_url, url)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Source object constructed from row
        '''
        return Source.create(row)

    def __init__(self, id:int = None, name:str = None, fixtures_url:str = None, url:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = SourceKeys(id)
        vals = SourceValues(name, fixtures_url, url)

        super().__init__('source', keys, vals)

    def getTable(self):
        return self._table

    def getId(self):
        return self._keys.id
    
    
    def getName(self):
        return self._vals.name
    
    def getFixtures_Url(self):
        return self._vals.fixtures_url
    
    def getUrl(self):
        return self._vals.url
    
    
    def setName(self, name:str):
       self._vals.name = name
    
    def setFixtures_Url(self, fixtures_url:str):
       self._vals.fixtures_url = fixtures_url
    
    def setUrl(self, url:str):
       self._vals.url = url
    
    

    def isNullable(self, field):
        if field == 'url':
            return True
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
