# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from Footy.src.database.database import Database, DatabaseInvObjError, \
         DatabaseKeys
from Footy.src.database.league import League
from Footy.src.database.sqlite3_db import SQLite3Impl, SQLite3DataError

class TestDatabase(TestCase):
    """Database tests"""

    def setUp(self):
        self.db = Database('../database/footy.test.db', SQLite3Impl())

    def tearDown(self):
        self.db.close()

    def test_select(self):
        leagues = self.db.select(League.asAdhoc(DatabaseKeys('league', None)))

        self.assertEqual(len(leagues), 2)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'English Prem'} : Values {'desc': 'The English Premier League'}")
        self.assertEqual(
                str(leagues[1]), "league : Keys {'name': 'English Champ'} : Values {'desc': 'The English Championship'}")

        leagues = self.db.select(League('"English Prem"'))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'English Prem'} : Values {'desc': 'The English Premier League'}")

        leagues = self.db.select(League.asAdhoc(DatabaseKeys('league', \
                {'desc': '"The English Championship"'})))
        self.assertEqual(len(leagues), 1)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'English Champ'} : Values {'desc': 'The English Championship'}")

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

        self.db.upsert(League('"English Prem"', '"Based right here"'))

        leagues = self.db.select(League.asAdhoc(DatabaseKeys('league', None)))

        self.assertEqual(len(leagues), 2)
        self.assertEqual(
                str(leagues[0]), "league : Keys {'name': 'English Prem'} : Values {'desc': 'Based right here'}")

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
