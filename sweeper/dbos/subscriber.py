from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class SubscriberKeys(DatabaseKeys):
    '''
    subscriber database object primary key representation
    '''
    email:str = None
    

    def __init__(self, email:str):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'email', email)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all SubscriberKeys fields
        '''
        fields = {} if None in (self.email,) else {'email' : self.email}
        return fields
        
class SubscriberValues(DatabaseValues):
    '''
    subscriber database object values representation
    '''
    def __init__(self, include:int, first_name:str = None, second_name:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'include', include)
        object.__setattr__(self, 'first_name', first_name)
        object.__setattr__(self, 'second_name', second_name)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all SubscriberValues fields
        '''
        fields = {'include' : self.include, 'first_name' : self.first_name, 'second_name' : self.second_name}
        return fields
        
class Subscriber(DatabaseObject):
    '''
    subscriber database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Subscriber object constructed via an AdhocKey of fields
        '''
        l = Subscriber()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Subscriber object constructed via an AdhocKey of fields
        '''
        return Subscriber.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Subscriber object constructed from row
        '''
        email, include, first_name, second_name = row
        return Subscriber(email, include, first_name, second_name)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Subscriber object constructed from row
        '''
        return Subscriber.create(row)

    def __init__(self, email:str = None, include:int = None, first_name:str = None, second_name:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = SubscriberKeys(email)
        vals = SubscriberValues(include, first_name, second_name)

        super().__init__('subscriber', keys, vals)

    def getTable(self):
        return self._table

    def getEmail(self):
        return self._keys.email
    
    
    def getInclude(self):
        return self._vals.include
    
    def getFirst_Name(self):
        return self._vals.first_name
    
    def getSecond_Name(self):
        return self._vals.second_name
    
    
    def setInclude(self, include:int):
       self._vals.include = include
    
    def setFirst_Name(self, first_name:str):
       self._vals.first_name = first_name
    
    def setSecond_Name(self, second_name:str):
       self._vals.second_name = second_name
    
    

    def isNullable(self, field):
        if field == 'first_name':
            return True
        elif field == 'second_name':
            return True
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
