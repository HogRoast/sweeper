import os
import tempfile
import webbrowser

class InvTableDefn(Exception):
    pass
    
class Table:
    STYLE = '<html>'\
            '<head>'\
            '<style>'\
            'table, th, td {'\
            '  border: 1px solid black;'\
            '  border-collapse: collapse;'\
            '}'\
            'th, td {'\
            '  padding: 5px;'\
            '}'\
            'caption{'\
            '  font: bold large sans-serif;'\
            '}'\
            '</style>'\
            '</head>'

    def __init__(self, headers:list=None, schema:list=None, rows:list=None,\
            highlights:list=None, title:str=None, style:str=STYLE,\
            htmlReplacements:list=None):
        self._headers = headers
        self._schema = schema
        self._rows = rows if rows else []
        self._highlights = self.setHighlights(highlights) if highlights else []
        self._title = title
        self._validate()
        self._style = style
        self._replacements = htmlReplacements

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

    def asHTML(self, show=False, fullyFormed=True):
        s = ''
        if self._title:
            s = '<caption>' + self._title + '</caption>'
        s += '<thead>'
        if self._schema:
            ss = '<tr><td>{}</td></tr>'.format('</td><td>'.join(self._schema))
        elif self._headers:
            ss = '<tr><th>{}</th></tr>'.format(\
                    ('{}</th><th>' * len(self._headers[0]))[:-9])
        elif self._rows:
            ss = '<tr><td>{}</td></tr>'.format(\
                    ('{}</td><td>' * len(self._rows[0]))[:-9])
        if self._headers:
            s += ss.replace('f', '').format(*self._headers)
            s = s.replace('td>', 'th>')
        s += '</thead><tbody>'
        # if schema has alignment formatting then convert this to HTML but only
        # for data cells
        ss = ss.replace('<td>{:>', '<td align="right">{:>')
        ss = ss.replace('<td>{:<', '<td align="left">{:<')
        for r in self._rows:
            sss = ss.format(*r)
            for (data, wholeRow) in self._highlights:
                if wholeRow and data in sss:
                    sss = sss.replace('<tr>', '<tr bgcolor=rgba(124,252,0,0.5)>')
                else:
                    sss = sss.replace(data, '<span style="background-color'\
                            ':lightgreen">{}</span>'.format(data))
            s += sss
        s += '</tbody>'

        if self._replacements:
            for r in self._replacements:
                if len(r) == 2:
                    s = s.replace(r[0], r[1])

        s = '<table>{}</table>'.format(s)
        if fullyFormed:
            s = '{}<body>{}</body>'.format(self._style, s)

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

    def addHighlight(self, highlight):
        if len(highlight) == 2:
            self._highlights.append(highlight)

    def setHighlights(self, highlights):
        [self.addHighlight(hl) for hl in highlights]

    def getHighlights(self):
        return self._highlights

    def getColumns(self):
        if not self._rows: return []
        return [[r[i] for r in self._rows] for i in range(len(self._rows[0]))]

    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self_title = title

    def htmlReplacements(self, replacements):
        self._replacements = replacements

    def __repr__(self):
        s = ''
        if self._title:
            s = '\033[1m{}\033[0m\n'.format(self._title)
        if self._schema:
            ss = '|'.join(self._schema)
        elif self._headers:
            ss = ('{}|' * len(self._headers))[:-1]
        elif self._rows:
            ss = ('{}|' * len(self._rows[0]))[:-1]
        if self._headers:
            lt = len(s)
            s += ss.replace('f', '').format(*self._headers)
            s += '\n' + ('-' * (len(s)-lt)) + '\n'
        ss += '\n'
        for r in self._rows:
            sss = ss.format(*r)
            for (data, wholeRow) in self._highlights:
                if wholeRow and data in r:
                    sss = '\033[1m{}\033[0m'.format(sss)
                else:
                    sss = sss.replace(data, '\033[1m{}\033[0m'.format(data))
            s += sss

        return s

if __name__ == '__main__':
    #t = Table()
    #t = Table(schema=['{:>4}', '{:>5}', '{:>3}'])
    t = Table(headers=['1st', '2nd', '3rd'], schema=['{:>4}', '{:>5.3f}', '{:>3}'], title='Test')
    t.append([[1, 2.454, 3], [4, 5, 6]])
    t.append([[7, 8, 'dfd']])
    t.setHighlights([['dfd', True]])
    t.addHighlight(['1', False])
    print(t.getRows())
    print(t.getColumns())
    print(t)
    print(t.asHTML(True))
