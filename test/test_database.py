# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from Footy.src.database.database import Database, DatabaseObject, \
        DatabaseInvObjError, AdhocKeys
from Footy.src.database.database_impl import DatabaseDataError, \
        DatabaseIntegrityError
from Footy.src.database.league import League
from Footy.src.database.team import Team
from Footy.src.database.sqlite3_db import SQLite3Impl

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
        self.assertEqual(leagues[1].getTable(), 'league')
        self.assertEqual(leagues[1].getName(), 'league name TD2')
        self.assertEqual(leagues[1].getDesc(), 'league desc TD2')

        leagues = TestDatabase.db.select(League('league name TD'))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD'} : Values {'desc': 'league desc TD'}")

        leagues = TestDatabase.db.select(
                League.createAdhoc(AdhocKeys({'desc': 'league desc TD2'})))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD2'} : Values {'desc': 'league desc TD2'}")

    def test_foreign_key(self):
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseIntegrityError) as cm:
            TestDatabase.db.upsert(Team('My Team', 'no such league'))
        self.assertEqual('FOREIGN KEY constraint failed', cm.exception.args[0])

    def test_transaction(self):
        # test commit
        with TestDatabase.db.transaction():
            TestDatabase.db.upsert(
                    League('My League', 'Based right here'))
            TestDatabase.db.upsert(
                    League('My League2', 'Also Based right here'))
        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 4)

        # test rollback on exception
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseDataError) as cm:
            TestDatabase.db.upsert(League('My League'))
        self.assertEqual(cm.exception.args[0], 'No values provided for UPDATE')
        self.assertEqual(len(leagues), 4)

        # test a forced rollback
        with TestDatabase.db.transaction() as t:
            TestDatabase.db.upsert(
                    League('My League3', 'Based right here'))
            t.fail()
        self.assertEqual(len(leagues), 4)

        # restore table to pre-test state
        with TestDatabase.db.transaction():
            TestDatabase.db.delete(League('My League'))
            TestDatabase.db.delete(League('My League2'))
        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 2)

    def test_select_NoRows(self):
        leagues = TestDatabase.db.select(League('Bundesliga'))
        self.assertEqual(len(leagues), 0)

    def test_upsert(self):
        with TestDatabase.db.transaction() as t:
            TestDatabase.db.upsert(League('My League', 'Based right here'))

            leagues = TestDatabase.db.select(League())

            self.assertEqual(len(leagues), 3)
            self.assertEqual(
                    str(leagues[2]), "league : Keys {'name': 'My League'} : Values {'desc': 'Based right here'}")

            TestDatabase.db.upsert(League('league name TD', 'Based right here'))

            leagues = TestDatabase.db.select(League('league name TD'))

            self.assertEqual(len(leagues), 1)
            self.assertEqual(
                    str(leagues[0]), "league : Keys {'name': 'league name TD'} : Values {'desc': 'Based right here'}")

            # force a rollback
            t.fail()

    def test_DatabaseObjectError(self):
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseInvObjError) as cm:
            leagues = TestDatabase.db.select(object())
        self.assertEqual(
                cm.exception.msg, 'Not a valid DB object : ' + str(object()))

    def test_upsert_Error(self):
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseDataError) as cm:
            TestDatabase.db.upsert(League())
        self.assertEqual(cm.exception.msg, 'No values provided for UPDATE')

    def test_delete(self):
        with TestDatabase.db.transaction():
            TestDatabase.db.upsert(
                    League('Bundesliga', 'The German Top Flight'))

        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 3)
        self.assertEqual(str(leagues[2]), "league : Keys {'name': 'Bundesliga'} : Values {'desc': 'The German Top Flight'}")

        with TestDatabase.db.transaction():
            TestDatabase.db.delete(League('Bundesliga'))
        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 2)

        leagues = TestDatabase.db.select(League('Bundesliga'))
        self.assertEqual(len(leagues), 0)
        
if __name__ == '__main__':
    import unittest
    unittest.main()
