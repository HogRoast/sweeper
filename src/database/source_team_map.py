from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class Source_Team_MapKeys(DatabaseKeys):
    '''
    source_team_map database object primary key representation
    '''
    source_id:int
    team:str
    

    def __init__(self, source_id:int, team:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'source_id', source_id)
        object.__setattr__(self, 'team', team)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all Source_Team_MapKeys fields
        '''
        fields = {} if not (self.source_id and self.team) else {'source_id' : self.source_id, 'team' : self.team}
        return fields
        
class Source_Team_MapValues(DatabaseValues):
    '''
    source_team_map database object values representation
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
        Get all the non-None value fields for this object in a dictionary form
        
        :returns: a dictionary of all Source_Team_MapValues fields
        '''
        fields = {'moniker' : self.moniker}
        fields = dict([(k, v) for (k, v) in fields.items() if v is not None])
        return fields
        
class Source_Team_Map(DatabaseObject):
    '''
    source_team_map database object representation
    '''

    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
        :returns: a Source_Team_Map object constructed via the primary key
        :raises: None
        '''
        l = Source_Team_Map()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private nstance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the primary key
        '''
        return Source_Team_Map.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_Team_Map object constructed from row
        '''
        source_id, team, moniker = row
        return Source_Team_Map(source_id, team, moniker)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_Team_Map object constructed from row
        '''
        return Source_Team_Map.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Source_Team_Map objects constructed from rows
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
        :returns: a list of Source_Team_Map objects constructed from rows
        '''
        return Source_Team_Map.createMulti(rows)

    def __init__(self, source_id:int = None, team:str = None, moniker:str = None):
        '''
        Construct the object from the provided table name, key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = Source_Team_MapKeys(source_id, team)
        vals = Source_Team_MapValues(moniker)

        super().__init__('source_team_map', keys, vals)

    def getTable(self):
        return self._table

    def getSource_Id(self):
        return self._keys.source_id
    
    def getTeam(self):
        return self._keys.team
    
    
    def getMoniker(self):
        return self._vals.moniker
    
    
    def setMoniker(self, moniker:str):
       self._vals.moniker = moniker
    
    

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
