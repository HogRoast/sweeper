from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class SeasonKeys(DatabaseKeys):
    '''
    season database object primary key representation
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
        
        :returns: a dictionary of all SeasonKeys fields
        '''
        fields = {} if not (self.name) else {'name' : self.name}
        return fields
        
class SeasonValues(DatabaseValues):
    '''
    season database object values representation
    '''
    def __init__(self, l_bnd_date:str = None, u_bnd_date:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'l_bnd_date', l_bnd_date)
        object.__setattr__(self, 'u_bnd_date', u_bnd_date)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the non-None value fields for this object in a dictionary form
        
        :returns: a dictionary of all SeasonValues fields
        '''
        fields = {'l_bnd_date' : self.l_bnd_date, 'u_bnd_date' : self.u_bnd_date}
        fields = dict([(k, v) for (k, v) in fields.items() if v is not None])
        return fields
        
class Season(DatabaseObject):
    '''
    season database object representation
    '''

    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
        :returns: a Season object constructed via the primary key
        :raises: None
        '''
        l = Season()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private nstance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the primary key
        '''
        return Season.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Season object constructed from row
        '''
        name, l_bnd_date, u_bnd_date = row
        return Season(name, l_bnd_date, u_bnd_date)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Season object constructed from row
        '''
        return Season.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Season objects constructed from rows
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
        :returns: a list of Season objects constructed from rows
        '''
        return Season.createMulti(rows)

    def __init__(self, name:str = None, l_bnd_date:str = None, u_bnd_date:str = None):
        '''
        Construct the object from the provided table name, key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = SeasonKeys(name)
        vals = SeasonValues(l_bnd_date, u_bnd_date)

        super().__init__('season', keys, vals)

    def getTable(self):
        return self._table

    def getName(self):
        return self._keys.name
    
    
    def getL_Bnd_Date(self):
        return self._vals.l_bnd_date
    
    def getU_Bnd_Date(self):
        return self._vals.u_bnd_date
    
    
    def setL_Bnd_Date(self, l_bnd_date:str):
       self._vals.l_bnd_date = l_bnd_date
    
    def setU_Bnd_Date(self, u_bnd_date:str):
       self._vals.u_bnd_date = u_bnd_date
    
    

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
