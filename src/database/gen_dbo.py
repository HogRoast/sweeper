import pprint

def createFile(tmplFilename, outFilename, replacements):
    print('Creating file...', tmplFilename, ' as ', outFilename)
    pprint.pprint(replacements, indent=4)

    # Open the template file for read and output file for writing
    with open(tmplFilename, 'r') as tmplFile, \
            open(outFilename, 'w') as outFile:
        for row in tmplFile:
            for r in replacements.keys():
                # Replace patterns
                i = row.find(r)
                if i > -1:
                    s = replacements[r]
                    # if the replacement pattern contains newlines then we 
                    # must ensure the indent is correct
                    if '\n' in s: 
                        spaces = str().join([' '] * i)
                        print('**** SHM **** ' + s)
                        s = s.replace('\n', '\n' + spaces)
                        print('**** SHM **** ' + s)
                    row = row.replace(r, s)
            outFile.write(row)

def createReplacements(table, fields):
    print('Creating replacements for...', table)
    pprint.pprint(fields, indent=4)

    replacements = {}
    replacements['{{TableName}}'] = table
    _Table = table[0].upper() + table[1:]
    replacements['{{CapTableName}}'] = _Table

    pkFieldsTyped = ''
    pkFieldsListTyped = ''
    pkFieldsAssign = ''
    pkFieldsAnd = ''
    pkFieldsDict = '{'
    pkTestDataList = ''
    pkTestDataAssign = ''
    pkTestDataAssertEqual = ''
    pkTestDataAssertEqual2 = ''
    pkTestDataDict = '{'
    valueFieldsListTypedAndDef = ''
    valueFieldsAssign = ''
    valueFieldsAnd = ''
    valueFieldsDict = '{'
    valueTestDataList = ''
    valueTestDataAssertEqual = ''
    valueTestDataAssertEqual2 = ''
    valueTestDataDict = '{'
    allFieldsList = ''
    allFieldsListTypedAndDef = ''
    allTestDataList = ''
    allTestDataList2 = ''
    allTestDataRows = ''
    for k, v in fields.items():
        type_ = 'str' if v[0] == 'char' else v[0]
        if v[1] == True:
            pkFieldsTyped += k + ':' + type_ +'\n'
            pkFieldsListTyped += k + ':' + type_ + ', '
            pkFieldsAssign += \
                    "object.__setattr__(self, '" + k +"', " + k + ')\n' 
            pkFieldsAnd += k + ' and '
            pkFieldsDict += "'" + k + "' : " + k + ', '  
            pkTestDataAssign += 'keys.' + k + ' = '
            pkTestDataAssertEqual += 'self.assertEqual(obj.keys.'
            pkTestDataAssertEqual2 += 'self.assertEqual(obj.keys.'
            pkTestDataDict += "'" + k + "': " 
            tmp = tmp2 = tmp3 = ''
            if v[0] == 'str':
                if v[2] is not None:
                    tmp = k + ", '" + v[2] + " TD')\n"
                    tmp3 = "'" + v[2] + " TD', "
                else:
                    tmp = k + ", '" + table + ' ' + k + " TD')\n"
                    tmp3 = "'" + table + ' ' + k + " TD', "
                pkTestDataList += tmp3 
                pkTestDataDict += tmp3
                pkTestDataAssign += "'Something New'\n"
                tmp2 = tmp.replace('TD', 'TD2')
            elif v[0] == 'int':
                pkTestDataList += '98, '
                pkTestDataAssign += '75\n' 
                pkTestDataDict += '98, '
                tmp = k + ', 98)\n'
                tmp2 = tmp.replace('98', '99')
            elif v[0] == 'float':
                pkTestDataList += '2.3, '
                pkTestDataAssign += '1.6\n' 
                pkTestDataDict += '2.3, '
                tmp = k + ', 2.3)\n'
                tmp2 = tmp.replace('2.3', '2.4')
            elif v[0] == 'char':
                pkTestDataList += "'X', "
                pkTestDataAssign += "'A'\n"
                pkTestDataDict += "'X', "
                tmp = k + ", 'X')\n"
                tmp2 = tmp.replace('X', 'Z')
            pkTestDataAssertEqual += tmp 
            pkTestDataAssertEqual2 += tmp2
        else:
            valueFieldsListTypedAndDef += k + ':' + type_ + ' = None, '
            valueFieldsAssign += \
                    "object.__setattr__(self, '" + k +"', " + k + ')\n' 
            valueFieldsAnd += k + ' and '
            valueFieldsDict += "'" + k + "' : " + k + ', '  
            valueTestDataDict += "'" + k + "': "
            valueTestDataAssertEqual += 'self.assertEqual(obj.vals.'
            valueTestDataAssertEqual2 += 'self.assertEqual(obj.vals.'
            tmp = tmp2 = tmp3 = ''
            if v[0] == 'str':
                if v[2] is not None:
                    tmp = k + ", '" + v[2] + " TD')\n"
                    tmp3 = "'" + v[2] + " TD', "
                else:
                    tmp = k + ", '" + table + ' ' + k + " TD')\n"
                    tmp3 = "'" + table + ' ' + k + " TD', "
                tmp2 = tmp.replace('TD', 'TD2')
                valueTestDataList += tmp3
                valueTestDataDict += tmp3
            elif v[0] == 'int':
                tmp = k + ', 98)\n'
                tmp2 = tmp.replace('98', '99')
                valueTestDataDict += '98, '
                valueTestDataList += '98, '
            elif v[0] == 'float':
                tmp = k + ', 2.3)\n'
                tmp2 = tmp.replace('2.3', '2.4')
                valueTestDataDict += '2.3, '
                valueTestDataList += '2.3, '
            elif v[0] == 'char':
                tmp = k + ", 'X')\n"
                tmp2 = tmp.replace('X', 'Z')
                valueTestDataDict += "'X', "
                valueTestDataList += "'X', "
            valueTestDataAssertEqual += tmp
            valueTestDataAssertEqual2 += tmp2

        allFieldsList += k + ', '
        allFieldsListTypedAndDef += k + ':' + type_ + ' = None, '
        if v[0] == 'str':
            if v[2] is not None:
                tmp = "'" + v[2] + " TD', "
            else:
                tmp = "'" + table + ' ' + k + " TD', "
            allTestDataList += tmp
            allTestDataList2 += tmp.replace('TD', 'TD2')
        elif v[0] == 'int':
            allTestDataList += '98, '
            allTestDataList2 += '99, '
        elif v[0] == 'float':
            allTestDataList += '2.3, '
            allTestDataList2 += '2.4, '
        elif v[0] == 'char':
            allTestDataList += "'X', "
            allTestDataList2 += "'Z', "

    # remove extraneous comma and other guff
    pkFieldsListTyped = pkFieldsListTyped[:-2]
    pkFieldsDict = pkFieldsDict[:-2] + '}'
    pkFieldsDictSelf = pkFieldsDict.replace(': ', ': self.')
    pkFieldsAnd = pkFieldsAnd[:-5]
    pkFieldsAndSelf = 'self.' + pkFieldsAnd
    pkFieldsAndSelf = pkFieldsAndSelf.replace(' and ', ' and self.')
    pkTestDataList = pkTestDataList[:-2]
    pkTestDataDict = pkTestDataDict[:-2] + '}'
    valueTestDataList = valueTestDataList[:-2]
    valueFieldsListTypedAndDef = valueFieldsListTypedAndDef[:-2]
    valueFieldsDict = valueFieldsDict[:-2] + '}'
    valueFieldsDictSelf = valueFieldsDict.replace(': ', ': self.')
    valueFieldsAnd = valueFieldsAnd[:-5]
    valueFieldsAndSelf = 'self. ' + valueFieldsAnd
    valueFieldsAndSelf = valueFieldsAndSelf.replace(' and ', ' and self.')
    valueTestDataDict = valueTestDataDict[:-2] + '}'
    allFieldsList = allFieldsList[:-2]
    allFieldsListTypedAndDef = allFieldsListTypedAndDef[:-2]
    allTestDataList = allTestDataList[:-2]
    allTestDataList2 = allTestDataList2[:-2]
    allTestDataRows = '(' + allTestDataList + '),\n' + '(' + allTestDataList2 + ')'
    newPKTestDataList = pkTestDataList.replace( \
                'TD', 'TD INS').replace('98', '100').replace( \
                '2.3', '5.6').replace('X', 'A')
    newPKTestDataDict = pkTestDataDict.replace( \
                'TD', 'TD INS').replace('98', '100').replace( \
                '2.3', '5.6').replace('X', 'A')
    newValueTestDataList = valueTestDataList.replace( \
                'TD', 'TD UPD').replace('98', '100').replace( \
                '2.3', '5.6').replace('X', 'A')
    newValueTestDataDict = valueTestDataDict.replace( \
                'TD', 'TD UPD').replace('98', '100').replace( \
                '2.3', '5.6').replace('X', 'A')

    replacements['{{PKFieldsTyped}}'] = pkFieldsTyped
    replacements['{{PKFieldsListTyped}}'] = pkFieldsListTyped
    replacements['{{PKFieldsAssign}}'] = pkFieldsAssign
    replacements['{{PKFieldsAnd}}'] = pkFieldsAnd
    replacements['{{PKFieldsAndSelf}}'] = pkFieldsAndSelf
    replacements['{{PKFieldsList}}'] = pkFieldsAnd.replace(' and', ',')
    replacements['{{PKFieldsDict}}'] = pkFieldsDict
    replacements['{{PKFieldsDictSelf}}'] = pkFieldsDictSelf
    replacements['{{PKTestDataList}}'] = pkTestDataList
    replacements['{{PKTestDataAssign}}'] = pkTestDataAssign
    replacements['{{PKTestDataAssertEqual}}'] = pkTestDataAssertEqual
    replacements['{{PKTestDataAssertEqualIdx0}}'] = \
            pkTestDataAssertEqual.replace('obj.', 'objs[0].')
    replacements['{{PKTestDataAssertEqualIdx1}}'] = \
            pkTestDataAssertEqual2.replace('obj.', 'objs[1].')
    replacements['{{PKTestDataDict}}'] = pkTestDataDict
    replacements['{{ValueTestDataList}}'] = valueTestDataList
    replacements['{{ValueFieldsListTypedAndDef}}'] = valueFieldsListTypedAndDef
    replacements['{{ValueFieldsAssign}}'] = valueFieldsAssign
    replacements['{{ValueFieldsAnd}}'] = valueFieldsAnd
    replacements['{{ValueFieldsAndSelf}}'] = valueFieldsAndSelf
    replacements['{{ValueFieldsList}}'] = valueFieldsAnd.replace(' and', ',')
    replacements['{{ValueFieldsDict}}'] = valueFieldsDict
    replacements['{{ValueFieldsDictSelf}}'] = valueFieldsDictSelf
    replacements['{{ValueTestDataAssertEqual}}'] = valueTestDataAssertEqual
    replacements['{{ValueTestDataAssertEqualIdx0}}'] = \
            valueTestDataAssertEqual.replace('obj.', 'objs[0].')
    replacements['{{ValueTestDataAssertEqualIdx1}}'] = \
            valueTestDataAssertEqual2.replace('obj.', 'objs[1].')
    replacements['{{ValueTestDataDict}}'] = valueTestDataDict
    replacements['{{AllFieldsList}}'] = allFieldsList
    replacements['{{AllFieldsListTypedAndDef}}'] = allFieldsListTypedAndDef
    replacements['{{AllTestDataList}}'] = allTestDataList
    replacements['{{AllTestDataRows}}'] = allTestDataRows
    replacements['{{NewValueTestDataList}}'] = newValueTestDataList
    replacements['{{NewValueTestDataDict}}'] = newValueTestDataDict
    replacements['{{NewPKTestDataList}}'] = newPKTestDataList
    replacements['{{NewPKTestDataDict}}'] = newPKTestDataDict

    return replacements

def generateDBO():
    # Open the database schema
    with open('../../database/create_db.sql', 'r') as dbFile:
        for row in dbFile:
            # Find CREATE TABLE commands
            if 'CREATE TABLE' in row:
                # Extract table name
                i = row.index('CREATE TABLE')
                j = row.index('(')
                table = row[i+13:j].strip()

                # Extract field lists with types - identify Primary Key fields
                fields = {}
                pk = []
                for row in dbFile:
                    # Look for the end of the table definition
                    if ');' in row:
                        break;
                    # Extract the field name
                    j = 0
                    t = None 
                    if 'text' in row: 
                        j = row.index('text')
                        t = 'str'
                    elif 'varchar' in row:
                        j = row.index('varchar')
                        t = 'str'
                    elif 'integer' in row:
                        j = row.index('integer')
                        t = 'int'
                    elif 'real' in row:
                        j = row.index('real')
                        t = 'float'
                    elif 'char' in row:
                        j = row.index('char')
                        t = 'char'
                    if j > 0:
                        f = row[:j].strip()
                        fields[f] = [t, False, None]

                    if 'primary key' in row or \
                            'PRIMARY KEY' in row:
                        i = row.index('(')
                        j = row.index(')')
                        pk = [x.strip() for x in row[i+1:j].split(',')]
                      
                    if 'foreign key' in row or \
                            'FOREIGN KEY' in row:
                        i = row.index('(')
                        j = row.index(')')
                        f = row[i+1:j].strip()
                        a = row.index('references ')
                        b = row.rindex('(')
                        c = row.rindex(')')
                        fields[f][2] = row[a+11:b] + ' ' + row[b+1:c]
                # Complete fields dict by assigning primary key property
                for f in fields:
                    if f in pk:
                        fields[f][1] = True
               
                # Create Template pattern replacements
                replacements = createReplacements(table, fields)
                createFile('./dbo_src.tmpl', './{}.py'.format(table), \
                        replacements)
                createFile('../../test/dbo_test.tmpl', \
                        '../../test/test_{}.py'.format(table), replacements)
                createFile('../../database/dbo_test_data.tmpl', \
                        '../../database/{}_test_data.sql'.format(table), \
                        replacements)

if __name__ == '__main__':
    generateDBO()
