# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.statistics import Statistics, StatisticsKeys, StatisticsValues
from Footy.src.database.database import DatabaseKeys

class TestStatistics(TestCase):
    """Statistics object tests"""

    @classmethod
    def setUpClass(cls):
        os.system('cat ../database/create_db.sql | sqlite3 ../database/footy.test.db')
        os.system('cat ../database/*_test_data.sql | sqlite3 ../database/footy.test.db')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_keys_Immutablility(self):
        keys =StatisticsKeys('statistics generation_date TD', 99, 'league name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.generation_date = 'Something New'
            keys.algo_id = 75
            keys.league = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Statistics.createAdhoc(DatabaseKeys('statistics', None))
        self.assertEqual(l.keys.table, 'statistics')
        self.assertTrue(l.keys.fields is None)

    def test_createSingle(self):
        obj = Statistics.createSingle(('statistics generation_date TD', 99, 'league name TD', 99, 99, 99, 99, 99))

        self.assertEqual(obj.keys.generation_date, 'statistics generation_date TD')
        self.assertEqual(obj.keys.algo_id, 99)
        self.assertEqual(obj.keys.league, 'league name TD')
         
        self.assertEqual(obj.vals.mark, 99)
        self.assertEqual(obj.vals.mark_freq, 99)
        self.assertEqual(obj.vals.home_freq, 99)
        self.assertEqual(obj.vals.away_freq, 99)
        self.assertEqual(obj.vals.draw_freq, 99)
         

    def test_createMulti(self):
        rows = [('statistics generation_date TD', 99, 'league name TD', 99, 99, 99, 99, 99),
                ('statistics generation_date TD2', 98, 'league name TD2', 98, 98, 98, 98, 98)]
        objs = Statistics.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.generation_date, 'statistics generation_date TD')
        self.assertEqual(objs[0].keys.algo_id, 99)
        self.assertEqual(objs[0].keys.league, 'league name TD')
        
        self.assertEqual(objs[0].vals.mark, 99)
        self.assertEqual(objs[0].vals.mark_freq, 99)
        self.assertEqual(objs[0].vals.home_freq, 99)
        self.assertEqual(objs[0].vals.away_freq, 99)
        self.assertEqual(objs[0].vals.draw_freq, 99)
        
        self.assertEqual(objs[1].keys.generation_date, 'statistics generation_date TD2')
        self.assertEqual(objs[1].keys.algo_id, 98)
        self.assertEqual(objs[1].keys.league, 'league name TD2')
        
        self.assertEqual(objs[1].vals.mark, 98)
        self.assertEqual(objs[1].vals.mark_freq, 98)
        self.assertEqual(objs[1].vals.home_freq, 98)
        self.assertEqual(objs[1].vals.away_freq, 98)
        self.assertEqual(objs[1].vals.draw_freq, 98)
        

    def test_repr(self):
        obj = Statistics('statistics generation_date TD', 99, 'league name TD', 99, 99, 99, 99, 99)
        self.assertEqual(str(obj), "statistics : Keys {'generation_date': 'statistics generation_date TD', 'algo_id': 99, 'league': 'league name TD'} : Values {'mark': 99, 'mark_freq': 99, 'home_freq': 99, 'away_freq': 99, 'draw_freq': 99}")

if __name__ == '__main__':
    import unittest
    unittest.main()
