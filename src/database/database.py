from dataclasses import dataclass
from itertools import chain
from abc import ABC, abstractmethod

class DatabaseInvObjError(Exception):
    '''
    An object provided to the database is invalid
    '''
    def __init__(self, msg):
        self.msg = msg

@dataclass(frozen=True)
class DatabaseKeys(ABC):
    '''
    An immutable abstract class to represent the primary key of a database 
    object
    '''
    def __init__(self, fields:dict):
        '''
        Constructor for an object with the given primary key fields

        :param fields: a dictionary of primary key fields
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, '_fields', fields)

    @abstractmethod
    def getFields(self):
        return self._fields

@dataclass(frozen=True)
class AdhocKeys(DatabaseKeys):
    '''
    A class to allow for adhoc selection outside of an objects primary key 
    fields
    '''
    def __init__(self, fields:dict):
        '''
        Constructor for an object with the given primary key fields

        :param fields: a dictionary of primary key fields
        '''
        super().__init__(fields)

    def getFields(self):
        return self._fields

class DatabaseValues(ABC):
    '''
    An abstract class to represent the value fields of a database object
    '''
    def __init__(self, fields:dict):
        '''
        Constructor for the given fields

        :param fields: a dictionary of data fields
        '''
        self._fields = fields

    @abstractmethod
    def getFields(self):
        return self._fields

class DatabaseObject(ABC):
    def __init__(self, table:str, keys:DatabaseKeys, values:DatabaseValues):
        '''
        Constructor for a database object representing the given table and
        primary key and values fields

        :param table: the underlying database table name
        :param keys: a DatabaseKeys object representing the primary key fields
        :param values: a DatabaseValues object representing the value fields
        '''
        self._table = table
        self._keys = keys
        self._vals = values

    @abstractmethod
    def _createAdhoc(self, keys:AdhocKeys):
        '''
        Abstract instance method to create a database object with the 
        provided adhoc keys list

        :param keys: an AdhocKeys object
        :returns: a League object constructed via the primary key
        '''
        pass

    @abstractmethod
    def _createSingle(cls, row:tuple):
        '''
        Abstract instance method to create a database object from the provided 
        database row

        :param row: a list of values representing the objects key and values
        :returns: a League object constructed from row
        '''
        pass

    @abstractmethod
    def _createMulti(cls, rows:tuple):
        '''
        Abstract instance method to create database objects from the provided 
        database rows

        :param rows: a list of lists of representing object keys and values
        :returns: a list of League objects constructed from rows
        '''
        pass

def isDatabaseKeys(fn):
    '''
    Decorator to ensure applicable methods are being passed a key object
    '''    
    def wrapper(*args, **kwargs):
        if isinstance(args[1], DatabaseKeys):
            return fn(*args, **kwargs)
        raise DatabaseInvObjError('Not a DB key object : ' + str(args[1]))
    return wrapper

def isDatabaseObject(fn):
    '''
    Decorator to ensure applicable methods are being passed a database object
    '''    
    def wrapper(*args, **kwargs):
        o = args[1]
        if isinstance(o, DatabaseObject):
            return fn(*args, **kwargs)
        raise DatabaseInvObjError('Not a valid DB object : ' + str(args[1]))
    return wrapper

class Database:
    '''
    Context manager enabled database class 
    '''
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._impl.close()
        return False

    def __init__(self, dbname, impl):
        '''
        Constructor for the given database and with the provided implementation

        :param dbname: a full path database name
        :param impl: a database implementation object instance
        '''
        self._dbname = dbname 
        self._impl = impl 
        self._impl.connect(self._dbname)
        # Default foreign keys to on
        self.enableForeignKeys()

    @isDatabaseObject
    def select(self, obj:DatabaseObject):
        '''
        Select from db the object(s) matching the provided object's key

        :param obj: a valid database object used to form the underlying SQL
        :returns: a list of database objects constructed from the selected rows
        :raises: DatabaseInvObjError if obj is not a valid DBO
        '''
        rows = self._impl.select(obj._table, obj._keys.getFields())
        return obj.createMulti(rows)

    @isDatabaseObject
    def upsert(self, obj:DatabaseObject):
        '''
        Insert or update the object into the database

        :param obj: a valid database object used to form the underlying SQL
        :raises: DatabaseInvObjError if obj is not a valid DBO
        :raises: DatabaseDataError underlying impl raises nothing to upsert
        '''
        if len(self.select(obj)) == 0:
            inserts = dict(chain(obj._keys.getFields().items(), \
                    obj._vals.getFields().items()))
            self._impl.insert(obj._table, inserts)
        else:
            self._impl.update(
                    obj._table, obj._vals.getFields(), obj._keys.getFields())

    @isDatabaseObject
    def delete(self, obj:DatabaseObject):
        '''
        Delete the object identified by the key from the database

        :param obj: a valid database object used to form the underlying SQL
        :raises: DatabaseInvObjError if obj is not a valid DBO
        '''
        self._impl.delete(obj._table, obj._keys.getFields())

    def enableForeignKeys(self):
        self._impl.execute('pragma foreign_keys=1')

    def disableForeignKeys(self):
        self._impl.execute('pragma foreign_keys=0')

    def execute(self, s:str):
        '''
        Execute the provided SQL against the underlying DB

        :param s: a SQL string
        :returns: the list of database rows affected, potentially empty
        :raises: DatabaseIntegrityError raised by impl if constraint is breached
        '''
        return self._impl.execute(s)

    def transaction(self):
        '''
        Create and return a database transaction object
        '''
        return Transaction(self)

    def close(self):
        '''
        Close the active database connection
        '''
        self._impl.close()

class Transaction:
    '''
    Context manager enabled database transaction class
    '''
    def __init__(self, db:Database):
        '''
        Constructor for the given database

        :param db: a Database object
        :returns: N/A
        :raises: None
        '''
        self._db = db
        self._fail = False

    def __enter__(self):
        self._db._impl.begin()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or self._fail:
            self._db._impl.rollback()
        else:
            self._db._impl.commit()
        return False

    def fail(self):
        '''
        Force a rollback by setting fail attribute True
        '''
        self._fail = True
