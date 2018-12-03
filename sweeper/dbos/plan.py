from dataclasses import dataclass
from shimbase.database import DatabaseObject, DatabaseKeys, DatabaseValues, AdhocKeys

@dataclass(frozen=True)
class PlanKeys(DatabaseKeys):
    '''
    plan database object primary key representation
    '''
    id:int = None
    

    def __init__(self, id:int):
        '''
        Construct the object from the provided primary key fields
        
        :param ...: typed primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'id', id)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the PK fields for this object in a dictionary form
        
        :returns: a dictionary of all PlanKeys fields
        '''
        fields = {} if None in (self.id,) else {'id' : self.id}
        return fields
        
class PlanValues(DatabaseValues):
    '''
    plan database object values representation
    '''
    def __init__(self, name:str, cost:float, desc:str = None):
        '''
        Construct the object from the provided value fields
        
        :param ...: typed value fields
        '''
        object.__setattr__(self, 'name', name)
        object.__setattr__(self, 'cost', cost)
        object.__setattr__(self, 'desc', desc)
        
        super().__init__(self.getFields())

    def getFields(self):
        '''
        Get all the value fields for this object in a dictionary form
        
        :returns: a dictionary of all PlanValues fields
        '''
        fields = {'name' : self.name, 'cost' : self.cost, 'desc' : self.desc}
        return fields
        
class Plan(DatabaseObject):
    '''
    plan database object representation
    '''

    @classmethod
    def createAdhoc(cls, fields:dict={}, order:tuple=None):
        '''
        Class method to create a database object with the provided adhoc 
        dictionary of fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Plan object constructed via an AdhocKey of fields
        '''
        l = Plan()
        l._keys = AdhocKeys(fields, order) 
        return l

    def _createAdhoc(self, fields:dict={}, order:tuple=None):
        '''
        Private instance method to create a database object with the 
        provided adhoc fields

        :param fields: a dictionary of fields
        :param order: a tuple of fields to order by, if prepended with '>' or \
                      '<' then desc or asc
        :returns: Plan object constructed via an AdhocKey of fields
        '''
        return Plan.createAdhoc(fields, order)

    @classmethod
    def create(cls, row:tuple):
        '''
        Class method to create a database object from the provided database row

        :param row: a list of values representing the objects key and values
        :returns: a Plan object constructed from row
        '''
        id, name, cost, desc = row
        return Plan(id, name, cost, desc)

    def _create(self, row:tuple):
        '''
        Private instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a Plan object constructed from row
        '''
        return Plan.create(row)

    def __init__(self, id:int = None, name:str = None, cost:float = None, desc:str = None):
        '''
        Construct the object from the provided key and value fields
        
        :param ...: typed key and value fields
        :returns: N/A
        :raises: None
        '''
        keys = PlanKeys(id)
        vals = PlanValues(name, cost, desc)

        super().__init__('plan', keys, vals)

    def getTable(self):
        return self._table

    def getId(self):
        return self._keys.id
    
    
    def getName(self):
        return self._vals.name
    
    def getCost(self):
        return self._vals.cost
    
    def getDesc(self):
        return self._vals.desc
    
    
    def setName(self, name:str):
       self._vals.name = name
    
    def setCost(self, cost:float):
       self._vals.cost = cost
    
    def setDesc(self, desc:str):
       self._vals.desc = desc
    
    

    def isNullable(self, field):
        if field == 'desc':
            return True
        
        return False

    def __repr__(self):
        return self._table + ' : Keys ' + str(self._keys.getFields()) + \
                ' : Values ' + str(self._vals.getFields())
