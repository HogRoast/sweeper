from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class Algo_ConfigKeys(DatabaseKeys):
    '''
    algo_config database object primary key representation
    '''
    config_date:str = None
    algo_id:int = None
    league:str = None
    

    def __init__(self, config_date:str, algo_id:int, league:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'config_date', config_date)
        object.__setattr__(self, 'algo_id', algo_id)
        object.__setattr__(self, 'league', league)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all Algo_ConfigKeys fields
        '''
        fields = {} if None in (self.config_date, self.algo_id, self.league,) else {'config_date' : self.config_date, 'algo_id' : self.algo_id, 'league' : self.league}
        return fields
        
class Algo_ConfigValues(DatabaseValues):
    '''
    algo_config database object values representation
    '''
    def __init__(self, l_bnd_mark:int, u_bnd_mark:int):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'l_bnd_mark', l_bnd_mark)
        object.__setattr__(self, 'u_bnd_mark', u_bnd_mark)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all Algo_ConfigValues fields
        '''
        fields = {'l_bnd_mark' : self.l_bnd_mark, 'u_bnd_mark' : self.u_bnd_mark}
        return fields
        
class Algo_Config(DatabaseObject):
    '''
    algo_config database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Algo_Config object constructed via an AdhocKey of fields
        '''
        l = Algo_Config()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Algo_Config object constructed via an AdhocKey of fields
        '''
        return Algo_Config.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Algo_Config object constructed from row
        '''
        config_date, algo_id, league, l_bnd_mark, u_bnd_mark = row
        return Algo_Config(config_date, algo_id, league, l_bnd_mark, u_bnd_mark)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Algo_Config object constructed from row
        '''
        return Algo_Config.create(row)

    def __init__(self, config_date:str = None, algo_id:int = None, league:str = None, l_bnd_mark:int = None, u_bnd_mark:int = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = Algo_ConfigKeys(config_date, algo_id, league)
        vals = Algo_ConfigValues(l_bnd_mark, u_bnd_mark)

        super().__init__('algo_config', keys, vals)

    def getTable(self):
        return self._table

    def getConfig_Date(self):
        return self._keys.config_date
    
    def getAlgo_Id(self):
        return self._keys.algo_id
    
    def getLeague(self):
        return self._keys.league
    
    
    def getL_Bnd_Mark(self):
        return self._vals.l_bnd_mark
    
    def getU_Bnd_Mark(self):
        return self._vals.u_bnd_mark
    
    
    def setL_Bnd_Mark(self, l_bnd_mark:int):
       self._vals.l_bnd_mark = l_bnd_mark
    
    def setU_Bnd_Mark(self, u_bnd_mark:int):
       self._vals.u_bnd_mark = u_bnd_mark
    
    

    def isNullable(self, field):
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
