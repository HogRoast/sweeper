from sqlite3 import connect

class SQLite3DataError(Exception):
    def __init__(self, msg):
        self.msg = msg

class SQLite3Impl:
    '''
    SQLite3 implementation class to be used with the generic Database class
    '''
    def connect(self, dbname:str):
        self._dbname = dbname
        self._conn = connect(dbname)

    def select(self, table:str, where:dict = None):
        '''
        Select from db the row(s) matching the provided fields or all rows if
        fields are None
        '''
        s = 'SELECT * FROM {} '.format(table)
        if where and len(where) > 0:
            s += 'WHERE '
            for k, v in where.items():
                if isinstance(v, str):
                    s += '{}="{}" and '.format(k, v) 
                else:
                    s += '{}={} and '.format(k, v) 
            # remove the extraneous ' and '
            s = s[:-5]
        print(s) 
        return self.execute(s)

    def insert(self, table:str, inserts:dict):
        '''
        Insert the given data into the database
        '''
        if inserts is None or len(inserts) == 0:
            raise SQLite3DataError('No values provided for INSERT')
    
        s = 'INSERT INTO {} ('.format(table)
        for k in inserts.keys():
            s += '{},'.format(k) 
        # remove the extraneous comma
        s = s[:-1]

        s += ') values ('
        for v in inserts.values():
            if isinstance(v, str):
                s += '"{}",'.format(v)
            else:
                s += '{},'.format(v)
        # remove the extraneous comma
        s = s[:-1]
        s += ')'

        self.execute(s)

    def update(self, table:str, updates:dict, where:dict = None):
        '''
        Update the fields whose row(s) are identified by the where dict
        '''
        if updates is None or len(updates) == 0:
            raise SQLite3DataError('No values provided for UPDATE')
        
        s = 'UPDATE {} SET '.format(table)
        for k, v in updates.items():
            if isinstance(v, str):
                s += '{}="{}",'.format(k, v) 
            else:
                s += '{}={},'.format(k, v) 
        # remove the extraneous comma
        s = s[:-1]

        if where and len(where) > 0:
            s += ' WHERE '
            for k, v in where.items():
                if isinstance(v, str):
                    s += '{}="{}" and '.format(k, v) 
                else:
                    s += '{}={} and '.format(k, v) 
            # remove the extraneous ' and '
            s = s[:-5]

        self.execute(s)

    def delete(self, table:str, where:dict = None):
        '''
        Delete the row(s) identified by the where dict
        '''
        s = 'DELETE FROM {} '.format(table)
        if where and len(where) > 0:
            s += 'WHERE '
            for k, v in where.items():
                if isinstance(v, str):
                    s += '{}="{}" and '.format(k, v) 
                else:
                    s += '{}={} and '.format(k, v) 
            # remove the extraneous ' and '
            s = s[:-5]

        self.execute(s)

    def execute(self, s):
        curs = self._conn.cursor()
        curs.execute(s)
        rows = curs.fetchall() 
        curs.close()

        return rows

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._conn.close()
