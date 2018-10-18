from dataclasses import dataclass
from itertools import chain

class DatabaseDataError(Exception):
    '''
    Data provided to the database is in error
    '''
    def __init__(self, msg):
        self.msg = msg

class DatabaseIntegrityError(Exception):
    '''
    A database constraint has been breached
    '''
    def __init__(self, msg):
        self.msg = msg

class DatabaseInvObjError(Exception):
    '''
    An object provided to the database is invalid
    '''
    def __init__(self, msg):
        self.msg = msg

@dataclass(frozen=True)
class DatabaseKeys:
    '''
    A class to represent the primary key of a database object
    '''
    def __init__(self, table:str, fields:dict):
        '''
        Constructor for provided table and with the given fields

        :param table: the database table this object represents
        :param fields: a dictionary of primary key fields
        :returns: N/A
        :raises: none
        '''
        # Need to use setattr as the class is Frozen (immutable)
        object.__setattr__(self, 'table', table)
        object.__setattr__(self, 'fields', fields)

class DatabaseValues:
    '''
    A class to represent the non primary key fields of a database object
    '''
    def __init__(self, fields:dict):
        '''
        Constructor for the given fields

        :param fields: a dictionary of data fields
        :returns: N/A
        :raises: none
        '''
        self.fields = fields

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
        d = dir(o)
        if 'keys' in d and 'vals' in d and 'createSingle' in d \
                and 'createMulti' in d:
            if isinstance(o.keys, DatabaseKeys) and \
                    isinstance(o.vals, DatabaseValues):
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
        :returns: N/A
        :raises: none
        '''
        self._dbname = dbname 
        self._impl = impl 
        self._impl.connect(self._dbname)
        # Default foreign keys to on
        self.enableForeignKeys()

    @isDatabaseObject
    def select(self, obj):
        '''
        Select from db the object(s) matching the provided object's key

        :param obj: a valid database object used to form the underlying SQL
        :returns: a list of database objects constructed from the selected rows
        :raises: DatabaseInvObjError if obj is not a valid DBO
        '''
        rows = self._impl.select(obj.keys.table, obj.keys.fields)
        return obj.createMulti(rows)

    @isDatabaseObject
    def upsert(self, obj):
        '''
        Insert or update the object into the database

        :param obj: a valid database object used to form the underlying SQL
        :returns: N/A
        :raises: DatabaseInvObjError if obj is not a valid DBO
        :raises: DatabaseDataError underlying impl raises nothing to upsert
        '''
        if len(self.select(obj)) == 0:
            inserts = dict(chain(obj.keys.fields.items(), \
                    obj.vals.fields.items()))
            self._impl.insert(obj.keys.table, inserts)
        else:
            self._impl.update(obj.keys.table, obj.vals.fields, obj.keys.fields)

    @isDatabaseObject
    def delete(self, obj):
        '''
        Delete the object identified by the key from the database

        :param obj: a valid database object used to form the underlying SQL
        :returns: N/A
        :raises: DatabaseInvObjError if obj is not a valid DBO
        '''
        self._impl.delete(obj.keys.table, obj.keys.fields)

    def enableForeignKeys(self):
        self._impl.execute('pragma foreign_keys=1')

    def disableForeignKeys(self):
        self._impl.execute('pragma foreign_keys=0')

    def execute(self, s):
        '''
        Execute the provided SQL against the underlying DB

        :param s: a SQL string
        :returns: the list of database rows affected, potentially empty
        :raises: DatabaseIntegrityError raised by impl if constraint is breached
        '''
        return self._impl.execute(s)

    def commit(self):
        self._impl.commit()

    def rollback(self):
        self._impl.rollback()

    def close(self):
        self._impl.close()
