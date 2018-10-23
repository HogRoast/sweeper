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
                str(leagues[0]), "league : Keys {'mnemonic': 'league mnemonic TD'} : Values {'name': 'league name TD', 'desc': 'league desc TD'}")
        self.assertEqual(leagues[1].getTable(), 'league')
        self.assertEqual(leagues[1].getMnemonic(), 'league mnemonic TD2')
        self.assertEqual(leagues[1].getName(), 'league name TD2')
        self.assertEqual(leagues[1].getDesc(), 'league desc TD2')

        leagues = TestDatabase.db.select(League('league mnemonic TD'))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'mnemonic': 'league mnemonic TD'} : Values {'name': 'league name TD', 'desc': 'league desc TD'}")

        leagues = TestDatabase.db.select(
                League.createAdhoc(AdhocKeys({'desc': 'league desc TD2'})))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'mnemonic': 'league mnemonic TD2'} : Values {'name': 'league name TD2', 'desc': 'league desc TD2'}")

    def test_foreign_key(self):
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseIntegrityError) as cm:
            TestDatabase.db.upsert(Team('My Team', 'no such league'))
        self.assertEqual('FOREIGN KEY constraint failed', cm.exception.args[0])

    def test_transaction(self):
        # test commit
        with TestDatabase.db.transaction():
            TestDatabase.db.upsert(
                    League('ML1', 'My League', 'Based right here'))
            TestDatabase.db.upsert(
                    League('ML2', 'My League2', 'Also Based right here'))
        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 4)

        # test rollback on exception
        with TestDatabase.db.transaction(), \
                self.assertRaises(DatabaseIntegrityError) as cm:
            TestDatabase.db.upsert(League('ML3'))
        self.assertEqual(cm.exception.args[0], 'NOT NULL constraint failed: league.name')
        self.assertEqual(len(leagues), 4)

        # test a forced rollback
        with TestDatabase.db.transaction() as t:
            TestDatabase.db.upsert(
                    League('ML4', 'My League4', 'Based right here'))
            t.fail()
        self.assertEqual(len(leagues), 4)

        # restore table to pre-test state
        with TestDatabase.db.transaction():
            TestDatabase.db.delete(League('ML1'))
            TestDatabase.db.delete(League('ML2'))
        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 2)

    def test_select_NoRows(self):
        leagues = TestDatabase.db.select(League('D1'))
        self.assertEqual(len(leagues), 0)

    def test_upsert(self):
        with TestDatabase.db.transaction() as t:
            TestDatabase.db.upsert(
                    League('ML1', 'My League', 'Based right here'))

            leagues = TestDatabase.db.select(League())

            self.assertEqual(len(leagues), 3)
            self.assertEqual(
                    str(leagues[2]), "league : Keys {'mnemonic': 'ML1'} : Values {'name': 'My League', 'desc': 'Based right here'}")

            TestDatabase.db.upsert(League( \
                    'league mnemonic TD', 'My League', desc='Based right here'))

            leagues = TestDatabase.db.select(League('league mnemonic TD'))

            self.assertEqual(len(leagues), 1)
            self.assertEqual(
                    str(leagues[0]), "league : Keys {'mnemonic': 'league mnemonic TD'} : Values {'name': 'My League', 'desc': 'Based right here'}")

            # force a rollback
            t.fail()

    def test_null(self):
        with TestDatabase.db.transaction() as t:
            TestDatabase.db.upsert(League('E1', 'English Champ'))

            leagues = TestDatabase.db.select(League('E1'))

            self.assertEqual(len(leagues), 1)
            self.assertEqual(
                    str(leagues[0]), "league : Keys {'mnemonic': 'E1'} : Values {'name': 'English Champ', 'desc': None}")

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
                self.assertRaises(DatabaseIntegrityError) as cm:
            TestDatabase.db.upsert(League())
        self.assertEqual(
                cm.exception.msg, 'NOT NULL constraint failed: league.name')

    def test_delete(self):
        with TestDatabase.db.transaction():
            TestDatabase.db.upsert(
                    League('D1', 'Bundesliga', 'The German Top Flight'))

        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 3)
        self.assertEqual(str(leagues[2]), "league : Keys {'mnemonic': 'D1'} : Values {'name': 'Bundesliga', 'desc': 'The German Top Flight'}")

        with TestDatabase.db.transaction():
            TestDatabase.db.delete(League('D1'))
        leagues = TestDatabase.db.select(League())
        self.assertEqual(len(leagues), 2)

        leagues = TestDatabase.db.select(League('D1'))
        self.assertEqual(len(leagues), 0)
        
if __name__ == '__main__':
    import unittest
    unittest.main()
