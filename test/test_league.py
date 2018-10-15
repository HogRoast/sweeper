# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.league import League, LeagueKeys, LeagueValues
from Footy.src.database.database import DatabaseKeys

class TestLeague(TestCase):
    """League object tests"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_keys_Immutablility(self):
        keys = LeagueKeys('English Prem')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.name = 'No Change'
        self.assertEqual(cm.exception.args[0], "cannot assign to field 'name'")

    def test_keys_adhoc(self):
        l = League.asAdhoc(DatabaseKeys('league', None))
        self.assertEquals(l.keys.table, 'league')
        self.assertTrue(l.keys.fields is None)

    def test_createSingle(self):
        obj = League.createSingle(
                ('English Prem', 'The English Premier League'))
        
        self.assertEqual(obj.keys.name, 'English Prem')
        self.assertEqual(obj.vals.desc, 'The English Premier League')

    def test_createMulti(self):
        rows = [('English Prem', 'The English Premier League'),
                ('English Champ', 'The English Championship')]
        objs = League.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.name, 'English Prem')
        self.assertEqual(objs[0].vals.desc, 'The English Premier League')
        self.assertEqual(objs[1].keys.name, 'English Champ')
        self.assertEqual(objs[1].vals.desc, 'The English Championship')

    def test_repr(self):
        obj = League('English Prem', 'The English Premier League')
        self.assertEqual(str(obj), "league : Keys {'name': 'English Prem'} : Values {'desc': 'The English Premier League'}")

if __name__ == '__main__':
    import unittest
    unittest.main()
