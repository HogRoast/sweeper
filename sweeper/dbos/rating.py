from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

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
    def __init__(self, algo_id:int, rank:int):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'algo_id', algo_id)
        object.__setattr__(self, 'rank', rank)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all RatingValues fields
        '''
        fields = {'algo_id' : self.algo_id, 'rank' : self.rank}
        return fields
        
class Rating(DatabaseObject):
    '''
    rating database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Rating object constructed via an AdhocKey of fields
        '''
        l = Rating()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Rating object constructed via an AdhocKey of fields
        '''
        return Rating.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Rating object constructed from row
        '''
        match_oid, algo_id, rank = row
        return Rating(match_oid, algo_id, rank)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Rating object constructed from row
        '''
        return Rating.create(row)

    def __init__(self, match_oid:int = None, algo_id:int = None, rank:int = None):
        '''
        Construct the object from the provided key and value fields
        
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
    
    

    def isNullable(self, field):
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
