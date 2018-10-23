from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class SourceKeys(DatabaseKeys):
    '''
    source database object primary key representation
    '''
    id:int
    

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
        fields = {} if not (self.id) else {'id' : self.id}
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
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
        :returns: a Source object constructed via the provided key
        :raises: None
        '''
        l = Source()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private instance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the provided key
        '''
        return Source.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Source object constructed from row
        '''
        id, name, fixtures_url, url = row
        return Source(id, name, fixtures_url, url)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Source object constructed from row
        '''
        return Source.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Source objects constructed from rows
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
        :returns: a list of Source objects constructed from rows
        '''
        return Source.createMulti(rows)

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
