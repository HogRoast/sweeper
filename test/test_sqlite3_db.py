# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from Footy.src.database.sqlite3_db import SQLite3Impl, SQLite3DataError

class TestSQLite3Impl(TestCase):
    """SQLite3Impl tests"""

    def setUp(self):
        self.db = SQLite3Impl()
        self.db.connect('../database/footy.test.db')

    def tearDown(self):
        self.db.close()

    def test_select(self):
        rows = self.db.select('league', {})    

        self.assertEqual(len(rows), 2)
        self.assertEqual(
                rows[0], ('English Prem', 'The English Premier League'))
        self.assertEqual(rows[1], ('English Champ', 'The English Championship'))

        rows = self.db.select('team', {'name' : '"Burnley"'})

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ('Burnley', 'English Prem'))

        rows = self.db.select('team', {'league' : '"English Champ"'})

        self.assertEqual(len(rows), 2)
        self.assertEqual(
                rows[0], ('Brentford', 'English Champ'))
        self.assertEqual(rows[1], ('Leeds', 'English Champ'))

    def test_select_NoRows(self):
        rows = self.db.select('team', {'name' : '"NoTeam"'})
        self.assertEqual(len(rows), 0)

    def test_insert(self):
        self.db.insert(
                'team', {'name' : '"my_team"', 'league' : '"English Champ"'})

        rows = self.db.select('team')

        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[4], ('my_team', 'English Champ'))

        self.db.rollback()

    def test_insert_Error(self):
        with self.assertRaises(SQLite3DataError) as cm:
            self.db.insert('team', {})
        self.assertEqual(cm.exception.msg, 'No values provided for INSERT')

    def test_update(self):
        self.db.update('league', {'desc' : '"New description"'}, \
                {'name' : '"English Prem"'})

        rows = self.db.select('league')

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ('English Prem', 'New description'))

        self.db.rollback()

    def test_update_Error(self):
        with self.assertRaises(SQLite3DataError) as cm:
            self.db.update('team', {})
        self.assertEqual(cm.exception.msg, 'No values provided for UPDATE')

    def test_delete(self):
        self.db.insert('league', {'name' : '"Bundesliga"', \
                'desc' : '"The German Top Flight"'})
        self.db.commit()

        rows = self.db.select('league')
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2], ('Bundesliga', 'The German Top Flight'))

        self.db.delete('league', {'name' : '"Bundesliga"'})
        self.db.commit()

        rows = self.db.select('league')
        self.assertEqual(len(rows), 2)

        rows = self.db.select('league', {'name' : '"Bundesliga"'})
        self.assertEqual(len(rows), 0)

if __name__ == '__main__':
    import unittest
    unittest.main()
