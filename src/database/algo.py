from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

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
        :returns: N/A
        :raises: None
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'id', id)
        
        fields = None if not (id) else {'id' : id}
        super().__init__('algo', fields)

class AlgoValues(DatabaseValues):
    '''
    algo database object values representation
    '''
    def __init__(self, name:str = None, desc:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        :returns: N/A
        :raises: None
        '''
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'desc', desc)
        
        fields = None if not (name and desc) else {'name' : name, 'desc' : desc}
        super().__init__(fields)

class Algo:
    '''
    algo database object representation
    '''
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        '''
        Class method to create a database object with the provided primary key

        :param keys: a DatabaseKeys object
        :returns: a Algo object constructed via the primary key
        :raises: None
        '''
        l = Algo()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Algo object constructed from row
        :raises: None
        '''
        id, name, desc = row
        return Algo(id, name, desc)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Algo objects constructed from rows
        :raises: None
        '''
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, id:int = None, name:str = None, desc:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        self.keys = AlgoKeys(id)
        self.vals = AlgoValues(name, desc)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
