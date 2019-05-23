import copy
import os
import re
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
        lines = iter(str(self).split('\n')[:-1])
        s = ''
        if self._title:
            next(lines)
            s = '<caption>' + self._title + '</caption>'
        if self._headers:
            s += '<thead><tr><th>'
            s += next(lines).replace('|', '</th><th>')
            s += '</th></tr></thead>'
            # jump the underline
            next(lines)
        if self._rows:
            s += '<tbody>'
            for l in lines:
                if l[:4] == '\033[1m' and l[-4:] == '\033[0m':
                    s += '<tr bgcolor=lightgreen><td>'
                else:
                    s += '<tr><td>'
                s += l.replace('|', '</td><td>')
                s += '</td></tr>'
            s += '</tbody>'

        # replace any remaining highlight codes
        s = s.replace('\033[1m', '<span style="background-color:lightgreen">')
        s = s.replace('\033[0m', '</span>')

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

    def addHighlight(self, col, pattern=None, wholeRow=False, repeat=True):  
        if isinstance(col, str):
            for i, h in enumerate(self._headers):
                if h == col:
                    col = i
                    self._highlights.append((col, pattern, wholeRow, repeat))
                    break
        elif isinstance(col, int):
            self._highlights.append((col, pattern, wholeRow, repeat))
        # sort the highlights so whole rows are managed first in the output
        self._highlights = sorted(self._highlights, key=lambda x : x[-1], \
            reverse=True)

    def setHighlights(self, highlights):
        [self.addHighlight(*hl) for hl in highlights]

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

        for i, r in enumerate(self._rows):
            sss = ss
            for j, (colIdx, pattern, wholeRow, repeat) in \
                    enumerate(self._highlights):
                if pattern is None or pattern == r[colIdx]:
                    if wholeRow:
                        sss = '\033[1m{}\033[0m\n'.format(ss[:-1])
                        break
                    else:
                        sss = sss.split('|')
                        sss[colIdx] = '\033[1m{}\033[0m'.format(sss[colIdx])
                        sss = '|'.join(sss)
                    if not repeat:
                        del self._highlights[j]
            s += sss.format(*r)

        return s

if __name__ == '__main__':
    #t = Table()
    #t = Table(schema=['{:>4}', '{:>5}', '{:>3}'])
    t = Table(headers=['1st', '2nd', '3rd'], schema=['{:>4}', '{:>5.3f}', '{:>3}'], title='Test')
    t.append([[1, 2.454, 3], [4, 5, 6]])
    t.append([[7, 8, 'dfd']])
    t.setHighlights([[1]])
    t.setHighlights([[2, 'dfd', True]])
    t.append([[75,3, 3]])
    t.addHighlight('3rd', 3, False, False)
    print(t.getRows())
    print(t.getColumns())
    print(t)
    print(t.asHTML(True))
