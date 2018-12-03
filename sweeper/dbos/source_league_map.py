from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class Source_League_MapKeys(DatabaseKeys):
    '''
    source_league_map database object primary key representation
    '''
    source_id:int = None
    league:str = None
    

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
        fields = {} if None in (self.source_id, self.league,) else {'source_id' : self.source_id, 'league' : self.league}
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
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Source_League_Map object constructed via an AdhocKey of fields
        '''
        l = Source_League_Map()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Source_League_Map object constructed via an AdhocKey of fields
        '''
        return Source_League_Map.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_League_Map object constructed from row
        '''
        source_id, league, moniker = row
        return Source_League_Map(source_id, league, moniker)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Source_League_Map object constructed from row
        '''
        return Source_League_Map.create(row)

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
