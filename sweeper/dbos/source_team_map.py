from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class Source_Team_MapKeys(DatabaseKeys):
    '''
    source_team_map database object primary key representation
    '''
    source_id:int = None
    moniker:str = None
    

    def __init__(self, source_id:int, moniker:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'source_id', source_id)
        object.__setattr__(self, 'moniker', moniker)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all Source_Team_MapKeys fields
        '''
        fields = {} if None in (self.source_id, self.moniker,) else {'source_id' : self.source_id, 'moniker' : self.moniker}
        return fields
        
class Source_Team_MapValues(DatabaseValues):
    '''
    source_team_map database object values representation
    '''
    def __init__(self, team:str):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'team', team)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all Source_Team_MapValues fields
        '''
        fields = {'team' : self.team}
        return fields
        
class Source_Team_Map(DatabaseObject):
    '''
    source_team_map database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Source_Team_Map object constructed via an AdhocKey of fields
        '''
        l = Source_Team_Map()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Source_Team_Map object constructed via an AdhocKey of fields
        '''
        return Source_Team_Map.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_Team_Map object constructed from row
        '''
        source_id, moniker, team = row
        return Source_Team_Map(source_id, moniker, team)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_Team_Map object constructed from row
        '''
        return Source_Team_Map.create(row)

    def __init__(self, source_id:int = None, moniker:str = None, team:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = Source_Team_MapKeys(source_id, moniker)
        vals = Source_Team_MapValues(team)

        super().__init__('source_team_map', keys, vals)

    def getTable(self):
        return self._table

    def getSource_Id(self):
        return self._keys.source_id
    
    def getMoniker(self):
        return self._keys.moniker
    
    
    def getTeam(self):
        return self._vals.team
    
    
    def setTeam(self, team:str):
       self._vals.team = team
    
    

    def isNullable(self, field):
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
