# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from Footy.src.database.database import Database, DatabaseInvObjError, \
         DatabaseKeys
from Footy.src.database.league import League
from Footy.src.database.sqlite3_db import SQLite3Impl, SQLite3DataError

class TestDatabase(TestCase):
    """Database tests"""

    @classmethod
    def setUpClass(cls):
        os.system('cat ../database/create_db.sql | sqlite3 ../database/footy.test.db')
        os.system('cat ../database/*_test_data.sql | sqlite3 ../database/footy.test.db')

    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        self.db = Database('../database/footy.test.db', SQLite3Impl())

    def tearDown(self):
        self.db.close()

    def test_select(self):
        leagues = self.db.select(League())

        self.assertEqual(len(leagues), 2)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD'} : Values {'desc': 'league desc TD'}")
        self.assertEqual(
                str(leagues[1]), "league : Keys {'name': 'league name TD2'} : Values {'desc': 'league desc TD2'}")

        leagues = self.db.select(League('"league name TD"'))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD'} : Values {'desc': 'league desc TD'}")

        leagues = self.db.select(League.createAdhoc(DatabaseKeys('league', \
                {'desc': '"league desc TD2"'})))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD2'} : Values {'desc': 'league desc TD2'}")

    def test_select_NoRows(self):
        leagues = self.db.select(League('"Bundesliga"'))
        self.assertEqual(len(leagues), 0)

    def test_upsert(self):
        self.db.upsert(League('"My League"', '"Based right here"'))

        leagues = self.db.select(League())

        self.assertEqual(len(leagues), 3)
        self.assertEqual(
                str(leagues[2]), "league : Keys {'name': 'My League'} : Values {'desc': 'Based right here'}")

        self.db.rollback()

        self.db.upsert(League('"league name TD"', '"Based right here"'))

        leagues = self.db.select(League())

        self.assertEqual(len(leagues), 2)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'league name TD'} : Values {'desc': 'Based right here'}")

        self.db.rollback()

    def test_DatabaseObjectError(self):
        with self.assertRaises(DatabaseInvObjError) as cm:
            leagues = self.db.select(object())
        self.assertEqual(cm.exception.msg, 'Not a valid DB object : ' + str(object()))

    def test_upsert_Error(self):
        with self.assertRaises(SQLite3DataError) as cm:
            self.db.upsert(League())
        self.assertEqual(cm.exception.msg, 'No values provided for UPDATE')

    def test_delete(self):
        self.db.upsert(League('"Bundesliga"', '"The German Top Flight"'))
        self.db.commit()

        leagues = self.db.select(League())
        self.assertEqual(len(leagues), 3)
        self.assertEqual(str(leagues[2]), "league : Keys {'name': 'Bundesliga'} : Values {'desc': 'The German Top Flight'}")

        self.db.delete(League('"Bundesliga"'))
        self.db.commit()

        leagues = self.db.select(League())
        self.assertEqual(len(leagues), 2)

        leagues = self.db.select(League('"Bundesliga"'))
        self.assertEqual(len(leagues), 0)
        
if __name__ == '__main__':
    import unittest
    unittest.main()
