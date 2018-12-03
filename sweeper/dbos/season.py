from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class SeasonKeys(DatabaseKeys):
    '''
    season database object primary key representation
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
        
        :returns: a dictionary of all SeasonKeys fields
        '''
        fields = {} if None in (self.name,) else {'name' : self.name}
        return fields
        
class SeasonValues(DatabaseValues):
    '''
    season database object values representation
    '''
    def __init__(self, l_bnd_date:str, u_bnd_date:str):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'l_bnd_date', l_bnd_date)
        object.__setattr__(self, 'u_bnd_date', u_bnd_date)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all SeasonValues fields
        '''
        fields = {'l_bnd_date' : self.l_bnd_date, 'u_bnd_date' : self.u_bnd_date}
        return fields
        
class Season(DatabaseObject):
    '''
    season database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Season object constructed via an AdhocKey of fields
        '''
        l = Season()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Season object constructed via an AdhocKey of fields
        '''
        return Season.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Season object constructed from row
        '''
        name, l_bnd_date, u_bnd_date = row
        return Season(name, l_bnd_date, u_bnd_date)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Season object constructed from row
        '''
        return Season.create(row)

    def __init__(self, name:str = None, l_bnd_date:str = None, u_bnd_date:str = None):
        '''
        Construct the object from the provided key and value fields
        
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
    
    

    def isNullable(self, field):
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
