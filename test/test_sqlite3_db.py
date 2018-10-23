# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from Footy.src.database.sqlite3_db import SQLite3Impl
from Footy.src.database.database_impl import DatabaseDataError, \
        DatabaseIntegrityError

class TestSQLite3Impl(TestCase):
    """SQLite3Impl tests"""
    db = None

    @classmethod
    def setUpClass(cls):
        createName = '../database/create_db.sql' 
        testDataName = '../database/*_test_data.sql' 
        dbName = '../database/footy.test.db'
        os.system('cat {} | sqlite3 {}'.format(createName, dbName))
        os.system('cat {} | sqlite3 {}'.format(testDataName, dbName))
        cls.db = SQLite3Impl()
        cls.db.connect(dbName)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def setUp(self):
        TestSQLite3Impl.db.execute('pragma foreign_keys=0')

    def tearDown(self):
        pass

    def test_select(self):
        rows = TestSQLite3Impl.db.select('league', {})    

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ( \
                'league mnemonic TD', 'league name TD', 'league desc TD'))
        self.assertEqual(rows[1], ( \
                'league mnemonic TD2', 'league name TD2', 'league desc TD2'))

        rows = TestSQLite3Impl.db.select('team', {'name' : 'team name TD2'})

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ('team name TD2', 'league mnemonic TD2'))

        rows = TestSQLite3Impl.db.select(
                'team', {'league' : 'league mnemonic TD'})

        self.assertEqual(len(rows), 1)
        self.assertEqual(
                rows[0], ('team name TD', 'league mnemonic TD'))
  
    def test_foreign_key(self):
        TestSQLite3Impl.db.execute('pragma foreign_keys=1')
        with self.assertRaises(DatabaseIntegrityError) as cm:
            TestSQLite3Impl.db.insert('team', 
                    {'name' : 'new team', 'league' : 'no such league'})
        TestSQLite3Impl.db.rollback()
        self.assertEqual(cm.exception.msg, 'FOREIGN KEY constraint failed')
 
    def test_select_NoRows(self):
        rows = TestSQLite3Impl.db.select('team', {'name' : 'NoTeam'})
        self.assertEqual(len(rows), 0)

    def test_insert(self):
        TestSQLite3Impl.db.insert(
                'team', {'name' : 'my_team', 'league' : 'E1'})

        rows = TestSQLite3Impl.db.select('team')

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2], ('my_team', 'E1'))

        TestSQLite3Impl.db.rollback()

    def test_transaction(self):
        TestSQLite3Impl.db.begin()

        TestSQLite3Impl.db.insert(
                'team', {'name' : 'my_team', 'league' : 'E1'})
        TestSQLite3Impl.db.insert(
                'team', {'name' : 'my_team2', 'league' : 'E1'})

        TestSQLite3Impl.db.commit()

        rows = TestSQLite3Impl.db.select('team', {})    
        self.assertEqual(len(rows), 4)

        TestSQLite3Impl.db.insert(
                'team', {'name' : 'my_team3', 'league' : 'E1'})

        rows = TestSQLite3Impl.db.select('team', {})    
        self.assertEqual(len(rows), 5)

        TestSQLite3Impl.db.rollback()

        rows = TestSQLite3Impl.db.select('team', {})    
        self.assertEqual(len(rows), 4)

    def test_transaction_Failure(self):
        TestSQLite3Impl.db.begin()

        TestSQLite3Impl.db.insert(
                'team', {'name' : 'my_team4', 'league' : 'E1'})
        try:
            TestSQLite3Impl.db.insert('team', None)
        except:
            pass

        rows = TestSQLite3Impl.db.select('team', {'name' : 'my_team4'})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ('my_team4', 'E1'))

        TestSQLite3Impl.db.rollback()

        rows = TestSQLite3Impl.db.select('team', {'name' : 'my_team4'})
        self.assertEqual(len(rows), 0)

    def test_insert_Error(self):
        with self.assertRaises(DatabaseDataError) as cm:
            TestSQLite3Impl.db.insert('team', {})
        self.assertEqual(cm.exception.msg, 'No values provided for INSERT')

    def test_update(self):
        TestSQLite3Impl.db.update('league', {'desc' : 'New description'}, \
                {'mnemonic' : 'league mnemonic TD'})

        rows = TestSQLite3Impl.db.select('league')

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ( \
                'league mnemonic TD', 'league name TD', 'New description'))

        TestSQLite3Impl.db.rollback()

    def test_update_Error(self):
        with self.assertRaises(DatabaseDataError) as cm:
            TestSQLite3Impl.db.update('team', {})
        self.assertEqual(
                cm.exception.msg, 'No values provided for UPDATE')

    def test_null_insert(self):
        TestSQLite3Impl.db.insert('league', \
                {'mnemonic' : 'E1', 'name' : 'English Champ'})

        rows = TestSQLite3Impl.db.select('league', {'mnemonic' : 'E1'})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ('E1', 'English Champ', None))

        TestSQLite3Impl.db.rollback()

    def test_null_update(self):
        TestSQLite3Impl.db.insert('league', \
                {'mnemonic' : 'E1', 'name' : 'English Champ', \
                'desc' : 'A new description'})

        TestSQLite3Impl.db.update('league', {'desc' : None}, \
                {'mnemonic' : 'E1'})

        rows = TestSQLite3Impl.db.select('league', {'mnemonic' : 'E1'})
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ('E1', 'English Champ', None))

        TestSQLite3Impl.db.rollback()

    def test_delete(self):
        TestSQLite3Impl.db.insert('league', \
                {'mnemonic' : 'D1', 'name' : 'Bundesliga', \
                'desc' : 'The German Top Flight'})
        TestSQLite3Impl.db.commit()

        rows = TestSQLite3Impl.db.select('league')
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2], ('D1', 'Bundesliga', 'The German Top Flight'))

        TestSQLite3Impl.db.delete('league', {'name' : 'Bundesliga'})
        TestSQLite3Impl.db.commit()

        rows = TestSQLite3Impl.db.select('league')
        self.assertEqual(len(rows), 2)

        rows = TestSQLite3Impl.db.select('league', {'name' : 'Bundesliga'})
        self.assertEqual(len(rows), 0)

if __name__ == '__main__':
    import unittest
    unittest.main()
