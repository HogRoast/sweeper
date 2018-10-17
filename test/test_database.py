# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from sqlite3 import IntegrityError
from Footy.src.database.database import Database, DatabaseInvObjError, \
         DatabaseKeys
from Footy.src.database.league import League
from Footy.src.database.team import Team
from Footy.src.database.sqlite3_db import SQLite3Impl, SQLite3DataError

class TestDatabase(TestCase):
    """Database tests"""
    db = None

    @classmethod
    def setUpClass(cls):
        createName = '../database/create_db.sql' 
        testDataName = '../database/*_test_data.sql' 
        dbName = '../database/footy.test.db'
        os.system('cat {} | sqlite3 {}'.format(createName, dbName))
        os.system('cat {} | sqlite3 {}'.format(testDataName, dbName))
        cls.db = Database(dbName, SQLite3Impl())

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
    
    def setUp(self):
        TestDatabase.db.enableForeignKeys()

    def tearDown(self):
        pass

    def test_select(self):
        leagues = TestDatabase.db.select(League())

        self.assertEqual(len(leagues), 2)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD'} : Values {'desc': 'league desc TD'}")
        self.assertEqual(
                str(leagues[1]), "league : Keys {'name': 'league name TD2'} : Values {'desc': 'league desc TD2'}")

        leagues = TestDatabase.db.select(League('league name TD'))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD'} : Values {'desc': 'league desc TD'}")

        leagues = TestDatabase.db.select(League.createAdhoc(DatabaseKeys(\
                'league', {'desc': 'league desc TD2'})))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD2'} : Values {'desc': 'league desc TD2'}")

    def test_foreign_key(self):
        with self.assertRaises(IntegrityError) as cm:
            TestDatabase.db.upsert(Team('My Team', 'no such league'))
        TestDatabase.db.rollback()
        self.assertEqual('FOREIGN KEY constraint failed', cm.exception.args[0])

    def test_select_NoRows(self):
        leagues = TestDatabase.db.select(League('Bundesliga'))
        self.assertEqual(len(leagues), 0)

    def test_upsert(self):
        TestDatabase.db.upsert(League('My League', 'Based right here'))

        leagues = TestDatabase.db.select(League())

        self.assertEqual(len(leagues), 3)
        self.assertEqual(
                str(leagues[2]), "league : Keys {'name': 'My League'} : Values {'desc': 'Based right here'}")

        TestDatabase.db.rollback()

        TestDatabase.db.upsert(League('league name TD', 'Based right here'))

        leagues = TestDatabase.db.select(League())

        self.assertEqual(len(leagues), 2)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD'} : Values {'desc': 'Based right here'}")

        TestDatabase.db.rollback()

    def test_DatabaseObjectError(self):
        with self.assertRaises(DatabaseInvObjError) as cm:
            leagues = TestDatabase.db.select(object())
        self.assertEqual(
                cm.exception.msg, 'Not a valid DB object : ' + str(object()))

    def test_upsert_Error(self):
        with self.assertRaises(SQLite3DataError) as cm:
            TestDatabase.db.upsert(League())
        self.assertEqual(cm.exception.msg, 'No values provided for UPDATE')

    def test_delete(self):
        TestDatabase.db.upsert(
                League('Bundesliga', 'The German Top Flight'))
        TestDatabase.db.commit()

        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 3)
        self.assertEqual(str(leagues[2]), "league : Keys {'name': 'Bundesliga'} : Values {'desc': 'The German Top Flight'}")

        TestDatabase.db.delete(League('Bundesliga'))
        TestDatabase.db.commit()

        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 2)

        leagues = TestDatabase.db.select(League('Bundesliga'))
        self.assertEqual(len(leagues), 0)
        
if __name__ == '__main__':
    import unittest
    unittest.main()
