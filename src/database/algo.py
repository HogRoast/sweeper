from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class AlgoKeys(DatabaseKeys):
    '''
    algo database object primary key representation
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
        
        :returns: a dictionary of all AlgoKeys fields
        '''
        fields = None if not (self.id) else {'id' : self.id}
        return fields
        
class AlgoValues(DatabaseValues):
    '''
    algo database object values representation
    '''
    def __init__(self, name:str = None, desc:str = None):
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
        
        :returns: a dictionary of all AlgoValues fields
        '''
        fields = None if not (self.name and self.desc) else {'name' : self.name, 'desc' : self.desc}
        return fields
        
class Algo(DatabaseObject):
    '''
    algo database object representation
    '''

    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
        :returns: a Algo object constructed via the primary key
        :raises: None
        '''
        l = Algo()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private nstance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the primary key
        '''
        return Algo.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Algo object constructed from row
        '''
        id, name, desc = row
        return Algo(id, name, desc)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Algo object constructed from row
        '''
        return Algo.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Algo objects constructed from rows
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
        :returns: a list of Algo objects constructed from rows
        '''
        return Algo.createMulti(rows)

    def __init__(self, id:int = None, name:str = None, desc:str = None):
        '''
        Construct the object from the provided table name, key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = AlgoKeys(id)
        vals = AlgoValues(name, desc)

        super().__init__('algo', keys, vals)

    def getTable(self):
        return self._table

    def getId(self):
        return self._keys.id
    
    
    def getName(self):
        return self._vals.name
    
    def getDesc(self):
        return self._vals.desc
    
    
    def setName(self, name:str):
       self._vals.name = name
    
    def setDesc(self, desc:str):
       self._vals.desc = desc
    
    

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
