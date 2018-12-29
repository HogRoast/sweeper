import os
import tempfile
import webbrowser

class InvTableDefn(Exception):
    pass
    
class Table:
    def __init__(self, headers:list=None, schema:list=None, rows:list=None):
        self._headers = headers
        self._schema = schema
        self._rows = rows if rows else []
        self._validate()

    def _validate(self):
        if self._rows and not all(map(\
                lambda x : len(x) == len(self._rows[0]), self._rows)):
            raise InvTableDefn('Length of rows')
        if self._rows:
            if self._schema:
                if len(self._schema) != len(self._rows[0]):
                    raise InvTableDefn('Length of schema & rows')
            if self._headers:
                if len(self._headers) != len(self._rows[0]):
                    raise InvTableDefn('Length of headers & rows')
        else:
            if self._schema and self._headers:
                if len(self._schema) != len(self._headers):
                    raise InvTableDefn('Length of headers & schema')
        return True

    def append(self, rows:list):
        [self._rows.append(r) for r in rows]
        self._validate()

    def remove(self, rows:list):
        [self._rows.remove(r) for r in rows]
        self._validate()

    def asHTML(self, show=False):
        s = ''
        if self._schema:
            ss = '<tr><td>{}</td></tr>'.format('</td><td>'.join(self._schema))
        elif self._headers:
            ss = '<tr><td>{}</td></tr>'.format(\
                    ('{}</td><td>' * len(self._headers))[:-9])
        elif self._rows:
            ss = '<tr><td>{}</td></tr>'.format(\
                    ('{}</td><td>' * len(self._rows[0]))[:-9])
        if self._headers:
            s += ss.format(*self._headers)
            s = s.replace('td>', 'th>')
        for r in self._rows:
            s += ss.format(*r)
        s = '<table border=3>' + s

        if show:
            fd, name = tempfile.mkstemp(suffix='.html', text=True)
            f = os.fdopen(fd, 'w')
            f.write(s)
            f.close()
            webbrowser.open(name)

        return s

    def getHeaders(self):
        return self._headers

    def setHeaders(self, headers):
        self._headers = headers
        self._validate()

    def getSchema(self):
        return self._schema

    def setSchema(self, schema):
        self._schema = schema
        self._validate()

    def getRows(self):
        return self._rows

    def setRows(self, rows:list):
        self._rows = rows
        self._validate()

    def getColumns(self):
        if not self._rows: return []
        return [[r[i] for r in self._rows] for i in range(len(self._rows[0]))]

    def __repr__(self):
        s = ''
        if self._schema:
            ss = '|'.join(self._schema)
        elif self._headers:
            ss = ('{}|' * len(self._headers))[:-1]
        elif self._rows:
            ss = ('{}|' * len(self._rows[0]))[:-1]
        if self._headers:
            s = ss.format(*self._headers)
            s += '\n' + ('-' * len(s)) + '\n'
        ss += '\n'
        for r in self._rows:
            s += ss.format(*r)
        return s

if __name__ == '__main__':
    #t = Table()
    #t = Table(schema=['{:>4}', '{:>5}', '{:>3}'])
    t = Table(headers=['1st', '2nd', '3rd'], schema=['{:>4}', '{:>5}', '{:>3}'])
    t.append([[1, 2, 3], [4, 5, 6]])
    t.append([[7, 8, 'dfd']])
    print(t.getRows())
    print(t.getColumns())
    print(t)
    print(t.asHTML(True))
