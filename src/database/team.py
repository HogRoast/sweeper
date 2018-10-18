from dataclasses import dataclass
from Footy.src.database.database import DatabaseKeys, DatabaseValues

@dataclass(frozen=True)
class TeamKeys(DatabaseKeys):
    '''
    team database object primary key representation
    '''
    name:str
    

    def __init__(self, name:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        :returns: N/A
        :raises: None
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'name', name)
        
        fields = None if not (name) else {'name' : name}
        super().__init__('team', fields)

class TeamValues(DatabaseValues):
    '''
    team database object values representation
    '''
    def __init__(self, league:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        :returns: N/A
        :raises: None
        '''
        object.__setattr__(self, 'league', league)
        
        fields = None if not (league) else {'league' : league}
        super().__init__(fields)

class Team:
    '''
    team database object representation
    '''
    @classmethod
    def createAdhoc(cls, keys:DatabaseKeys):
        '''
        Class method to create a database object with the provided primary key

        :param keys: a DatabaseKeys object
        :returns: a Team object constructed via the primary key
        :raises: None
        '''
        l = Team()
        l.keys = keys
        return l

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Team object constructed from row
        :raises: None
        '''
        name, league = row
        return Team(name, league)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Team objects constructed from rows
        :raises: None
        '''
        l = []
        for r in rows:
            l.append(cls.createSingle(r))
        return l

    def __init__(self, name:str = None, league:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        self.keys = TeamKeys(name)
        self.vals = TeamValues(league)

    def __repr__(self):
        return self.keys.table + ' : Keys ' + str(self.keys.fields) + \
                ' : Values ' + str(self.vals.fields)
