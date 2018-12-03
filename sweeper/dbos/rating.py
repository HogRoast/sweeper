from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class RatingKeys(DatabaseKeys):
    '''
    rating database object primary key representation
    '''
    match_id:int = None
    algo_id:int = None
    

    def __init__(self, match_id:int, algo_id:int):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'match_id', match_id)
        object.__setattr__(self, 'algo_id', algo_id)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all RatingKeys fields
        '''
        fields = {} if None in (self.match_id, self.algo_id,) else {'match_id' : self.match_id, 'algo_id' : self.algo_id}
        return fields
        
class RatingValues(DatabaseValues):
    '''
    rating database object values representation
    '''
    def __init__(self, mark:int):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'mark', mark)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all RatingValues fields
        '''
        fields = {'mark' : self.mark}
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
        match_id, algo_id, mark = row
        return Rating(match_id, algo_id, mark)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Rating object constructed from row
        '''
        return Rating.create(row)

    def __init__(self, match_id:int = None, algo_id:int = None, mark:int = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = RatingKeys(match_id, algo_id)
        vals = RatingValues(mark)

        super().__init__('rating', keys, vals)

    def getTable(self):
        return self._table

    def getMatch_Id(self):
        return self._keys.match_id
    
    def getAlgo_Id(self):
        return self._keys.algo_id
    
    
    def getMark(self):
        return self._vals.mark
    
    
    def setMark(self, mark:int):
       self._vals.mark = mark
    
    

    def isNullable(self, field):
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
