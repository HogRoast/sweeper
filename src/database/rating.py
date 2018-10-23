from dataclasses import dataclass
from Footy.src.database.database import DatabaseObject, DatabaseKeys, \
        DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class RatingKeys(DatabaseKeys):
    '''
    rating database object primary key representation
    '''
    match_oid:int
    

    def __init__(self, match_oid:int):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'match_oid', match_oid)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all RatingKeys fields
        '''
        fields = {} if not (self.match_oid) else {'match_oid' : self.match_oid}
        return fields
        
class RatingValues(DatabaseValues):
    '''
    rating database object values representation
    '''
    def __init__(self, algo_id:int = None, rank:int = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'algo_id', algo_id)
        object.__setattr__(self, 'rank', rank)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the non-None value fields for this object in a dictionary form
        
        :returns: a dictionary of all RatingValues fields
        '''
        fields = {'algo_id' : self.algo_id, 'rank' : self.rank}
        fields = dict([(k, v) for (k, v) in fields.items() if v is not None])
        return fields
        
class Rating(DatabaseObject):
    '''
    rating database object representation
    '''

    @classmethod
    def createAdhoc(cls, keys:AdhocKeys):
        '''
        Class method to create a database object with the provided adhoc keys
        list

        :param keys: an AdhocKeys object
        :returns: a Rating object constructed via the primary key
        :raises: None
        '''
        l = Rating()
        l._keys = keys
        return l

    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Private nstance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the primary key
        '''
        return Rating.createAdhoc(keys)

    @classmethod
    def createSingle(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Rating object constructed from row
        '''
        match_oid, algo_id, rank = row
        return Rating(match_oid, algo_id, rank)

    def _createSingle(cls, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Rating object constructed from row
        '''
        return Rating.createSingle(row)

    @classmethod
    def createMulti(cls, rows:tuple):
        '''
        Class method to create database objects from the provided database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of Rating objects constructed from rows
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
        :returns: a list of Rating objects constructed from rows
        '''
        return Rating.createMulti(rows)

    def __init__(self, match_oid:int = None, algo_id:int = None, rank:int = None):
        '''
        Construct the object from the provided table name, key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = RatingKeys(match_oid)
        vals = RatingValues(algo_id, rank)

        super().__init__('rating', keys, vals)

    def getTable(self):
        return self._table

    def getMatch_Oid(self):
        return self._keys.match_oid
    
    
    def getAlgo_Id(self):
        return self._vals.algo_id
    
    def getRank(self):
        return self._vals.rank
    
    
    def setAlgo_Id(self, algo_id:int):
       self._vals.algo_id = algo_id
    
    def setRank(self, rank:int):
       self._vals.rank = rank
    
    

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
