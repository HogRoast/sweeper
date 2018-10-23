from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class Source_Season_MapKeys(DatabaseKeys):
    '''
    source_season_map database object primary key representation
    '''
    source_id:int
    season:str
    

    def __init__(self, source_id:int, season:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'source_id', source_id)
        object.__setattr__(self, 'season', season)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all Source_Season_MapKeys fields
        '''
        fields = {} if not (self.source_id and self.season) else {'source_id' : self.source_id, 'season' : self.season}
        return fields
        
class Source_Season_MapValues(DatabaseValues):
    '''
    source_season_map database object values representation
    '''
    def __init__(self, moniker:str = None, data_url:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'moniker', moniker)
        object.__setattr__(self, 'data_url', data_url)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the non-None value fields for this object in a dictionary form
        
        :returns: a dictionary of all Source_Season_MapValues fields
        '''
        fields = {'moniker' : self.moniker, 'data_url' : self.data_url}
        fields = dict([(k, v) for (k, v) in fields.items() if v is not None])
        return fields
        
class Source_Season_Map(DatabaseObject):
    '''
    source_season_map database object representation
    '''

    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
        :returns: a Source_Season_Map object constructed via the primary key
        :raises: None
        '''
        l = Source_Season_Map()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private nstance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the primary key
        '''
        return Source_Season_Map.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_Season_Map object constructed from row
        '''
        source_id, season, moniker, data_url = row
        return Source_Season_Map(source_id, season, moniker, data_url)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_Season_Map object constructed from row
        '''
        return Source_Season_Map.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Source_Season_Map objects constructed from rows
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
        :returns: a list of Source_Season_Map objects constructed from rows
        '''
        return Source_Season_Map.createMulti(rows)

    def __init__(self, source_id:int = None, season:str = None, moniker:str = None, data_url:str = None):
        '''
        Construct the object from the provided table name, key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = Source_Season_MapKeys(source_id, season)
        vals = Source_Season_MapValues(moniker, data_url)

        super().__init__('source_season_map', keys, vals)

    def getTable(self):
        return self._table

    def getSource_Id(self):
        return self._keys.source_id
    
    def getSeason(self):
        return self._keys.season
    
    
    def getMoniker(self):
        return self._vals.moniker
    
    def getData_Url(self):
        return self._vals.data_url
    
    
    def setMoniker(self, moniker:str):
       self._vals.moniker = moniker
    
    def setData_Url(self, data_url:str):
       self._vals.data_url = data_url
    
    

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
