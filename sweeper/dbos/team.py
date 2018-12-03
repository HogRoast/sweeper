from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class TeamKeys(DatabaseKeys):
    '''
    team database object primary key representation
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
        
        :returns: a dictionary of all TeamKeys fields
        '''
        fields = {} if None in (self.name,) else {'name' : self.name}
        return fields
        
class TeamValues(DatabaseValues):
    '''
    team database object values representation
    '''
    def __init__(self, league:str):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'league', league)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all TeamValues fields
        '''
        fields = {'league' : self.league}
        return fields
        
class Team(DatabaseObject):
    '''
    team database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Team object constructed via an AdhocKey of fields
        '''
        l = Team()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Team object constructed via an AdhocKey of fields
        '''
        return Team.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Team object constructed from row
        '''
        name, league = row
        return Team(name, league)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Team object constructed from row
        '''
        return Team.create(row)

    def __init__(self, name:str = None, league:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = TeamKeys(name)
        vals = TeamValues(league)

        super().__init__('team', keys, vals)

    def getTable(self):
        return self._table

    def getName(self):
        return self._keys.name
    
    
    def getLeague(self):
        return self._vals.league
    
    
    def setLeague(self, league:str):
       self._vals.league = league
    
    

    def isNullable(self, field):
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
