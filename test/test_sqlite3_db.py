# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from Footy.src.database.sqlite3_db import SQLite3Impl, SQLite3DataError

class TestSQLite3Impl(TestCase):
    """SQLite3Impl tests"""

    @classmethod
    def setUpClass(cls):
        os.system('cat ../database/create_db.sql | sqlite3 ../database/footy.test.db')
        os.system('cat ../database/*_test_data.sql | sqlite3 ../database/footy.test.db')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.db = SQLite3Impl()
        self.db.connect('../database/footy.test.db')

    def tearDown(self):
        self.db.close()

    def test_select(self):
        rows = self.db.select('league', {})    

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ('league name TD', 'league desc TD'))
        self.assertEqual(rows[1], ('league name TD2', 'league desc TD2'))

        rows = self.db.select('team', {'name' : '"team name TD2"'})

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ('team name TD2', 'league name TD2'))

        rows = self.db.select('team', {'league' : '"league name TD"'})

        self.assertEqual(len(rows), 1)
        self.assertEqual(
                rows[0], ('team name TD', 'league name TD'))

    def test_select_NoRows(self):
        rows = self.db.select('team', {'name' : '"NoTeam"'})
        self.assertEqual(len(rows), 0)

    def test_insert(self):
        self.db.insert(
                'team', {'name' : '"my_team"', 'league' : '"English Champ"'})

        rows = self.db.select('team')

        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[2], ('my_team', 'English Champ'))

        self.db.rollback()

    def test_insert_Error(self):
        with self.assertRaises(SQLite3DataError) as cm:
            self.db.insert('team', {})
        self.assertEqual(cm.exception.msg, 'No values provided for INSERT')

    def test_update(self):
        self.db.update('league', {'desc' : '"New description"'}, \
                {'name' : '"league name TD"'})

        rows = self.db.select('league')

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ('league name TD', 'New description'))

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
