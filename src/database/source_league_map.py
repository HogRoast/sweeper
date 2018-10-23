from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class Source_League_MapKeys(DatabaseKeys):
    '''
    source_league_map database object primary key representation
    '''
    source_id:int
    league:str
    

    def __init__(self, source_id:int, league:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'source_id', source_id)
        object.__setattr__(self, 'league', league)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all Source_League_MapKeys fields
        '''
        fields = {} if not (self.source_id and self.league) else {'source_id' : self.source_id, 'league' : self.league}
        return fields
        
class Source_League_MapValues(DatabaseValues):
    '''
    source_league_map database object values representation
    '''
    def __init__(self, moniker:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'moniker', moniker)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all Source_League_MapValues fields
        '''
        fields = {'moniker' : self.moniker}
        return fields
        
class Source_League_Map(DatabaseObject):
    '''
    source_league_map database object representation
    '''

    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
        :returns: a Source_League_Map object constructed via the provided key
        :raises: None
        '''
        l = Source_League_Map()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private instance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the provided key
        '''
        return Source_League_Map.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_League_Map object constructed from row
        '''
        source_id, league, moniker = row
        return Source_League_Map(source_id, league, moniker)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_League_Map object constructed from row
        '''
        return Source_League_Map.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Source_League_Map objects constructed from rows
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
        :returns: a list of Source_League_Map objects constructed from rows
        '''
        return Source_League_Map.createMulti(rows)

    def __init__(self, source_id:int = None, league:str = None, moniker:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = Source_League_MapKeys(source_id, league)
        vals = Source_League_MapValues(moniker)

        super().__init__('source_league_map', keys, vals)

    def getTable(self):
        return self._table

    def getSource_Id(self):
        return self._keys.source_id
    
    def getLeague(self):
        return self._keys.league
    
    
    def getMoniker(self):
        return self._vals.moniker
    
    
    def setMoniker(self, moniker:str):
       self._vals.moniker = moniker
    
    

    def isNullable(self, field):
        if field == 'league':
            return True
        elif field == 'moniker':
            return True
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
