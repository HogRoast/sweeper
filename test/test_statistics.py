# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.statistics import Statistics, StatisticsKeys, StatisticsValues
from Footy.src.database.database import Database, DatabaseKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestStatistics(TestCase):
    """Statistics object tests"""
    db = None

    @classmethod
    def setUpClass(cls):
        createName = '../database/create_db.sql' 
        testDataName = '../database/*_test_data.sql' 
        dbName = '../database/footy.test.db'
        os.system('cat {} | sqlite3 {}'.format(createName, dbName))
        os.system('cat {} | sqlite3 {}'.format(testDataName, dbName))
        cls.db = Database(dbName, SQLite3Impl())
        cls.db.enableForeignKeys()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_keys_Immutablility(self):
        keys =StatisticsKeys('statistics generation_date TD', 98, 'league name TD')

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
        obj = Statistics.createSingle(('statistics generation_date TD', 98, 'league name TD', 98, 98, 98, 98, 98))

        self.assertEqual(obj.keys.generation_date, 'statistics generation_date TD')
        self.assertEqual(obj.keys.algo_id, 98)
        self.assertEqual(obj.keys.league, 'league name TD')
         
        self.assertEqual(obj.vals.mark, 98)
        self.assertEqual(obj.vals.mark_freq, 98)
        self.assertEqual(obj.vals.home_freq, 98)
        self.assertEqual(obj.vals.away_freq, 98)
        self.assertEqual(obj.vals.draw_freq, 98)
         

    def test_createMulti(self):
        rows = [('statistics generation_date TD', 98, 'league name TD', 98, 98, 98, 98, 98),
                ('statistics generation_date TD2', 99, 'league name TD2', 99, 99, 99, 99, 99)]
        objs = Statistics.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.generation_date, 'statistics generation_date TD')
        self.assertEqual(objs[0].keys.algo_id, 98)
        self.assertEqual(objs[0].keys.league, 'league name TD')
        
        self.assertEqual(objs[0].vals.mark, 98)
        self.assertEqual(objs[0].vals.mark_freq, 98)
        self.assertEqual(objs[0].vals.home_freq, 98)
        self.assertEqual(objs[0].vals.away_freq, 98)
        self.assertEqual(objs[0].vals.draw_freq, 98)
        
        self.assertEqual(objs[1].keys.generation_date, 'statistics generation_date TD2')
        self.assertEqual(objs[1].keys.algo_id, 99)
        self.assertEqual(objs[1].keys.league, 'league name TD2')
        
        self.assertEqual(objs[1].vals.mark, 99)
        self.assertEqual(objs[1].vals.mark_freq, 99)
        self.assertEqual(objs[1].vals.home_freq, 99)
        self.assertEqual(objs[1].vals.away_freq, 99)
        self.assertEqual(objs[1].vals.draw_freq, 99)
        

    def test_repr(self):
        obj = Statistics('statistics generation_date TD', 98, 'league name TD', 98, 98, 98, 98, 98)
        self.assertEqual(str(obj), "statistics : Keys {'generation_date': 'statistics generation_date TD', 'algo_id': 98, 'league': 'league name TD'} : Values {'mark': 98, 'mark_freq': 98, 'home_freq': 98, 'away_freq': 98, 'draw_freq': 98}")

    def test_select(self):
        objs = TestStatistics.db.select(Statistics())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.generation_date, 'statistics generation_date TD')
        self.assertEqual(objs[0].keys.algo_id, 98)
        self.assertEqual(objs[0].keys.league, 'league name TD')
        
        self.assertEqual(objs[0].vals.mark, 98)
        self.assertEqual(objs[0].vals.mark_freq, 98)
        self.assertEqual(objs[0].vals.home_freq, 98)
        self.assertEqual(objs[0].vals.away_freq, 98)
        self.assertEqual(objs[0].vals.draw_freq, 98)
        
        self.assertEqual(objs[1].keys.generation_date, 'statistics generation_date TD2')
        self.assertEqual(objs[1].keys.algo_id, 99)
        self.assertEqual(objs[1].keys.league, 'league name TD2')
        
        self.assertEqual(objs[1].vals.mark, 99)
        self.assertEqual(objs[1].vals.mark_freq, 99)
        self.assertEqual(objs[1].vals.home_freq, 99)
        self.assertEqual(objs[1].vals.away_freq, 99)
        self.assertEqual(objs[1].vals.draw_freq, 99)
        
        
        objs = TestStatistics.db.select(Statistics('statistics generation_date TD', 98, 'league name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.generation_date, 'statistics generation_date TD')
        self.assertEqual(objs[0].keys.algo_id, 98)
        self.assertEqual(objs[0].keys.league, 'league name TD')
        
        self.assertEqual(objs[0].vals.mark, 98)
        self.assertEqual(objs[0].vals.mark_freq, 98)
        self.assertEqual(objs[0].vals.home_freq, 98)
        self.assertEqual(objs[0].vals.away_freq, 98)
        self.assertEqual(objs[0].vals.draw_freq, 98)
        

        objs = TestStatistics.db.select(Statistics.createAdhoc(DatabaseKeys('statistics', {'mark': 98, 'mark_freq': 98, 'home_freq': 98, 'away_freq': 98, 'draw_freq': 98})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.generation_date, 'statistics generation_date TD')
        self.assertEqual(objs[0].keys.algo_id, 98)
        self.assertEqual(objs[0].keys.league, 'league name TD')
        
        self.assertEqual(objs[0].vals.mark, 98)
        self.assertEqual(objs[0].vals.mark_freq, 98)
        self.assertEqual(objs[0].vals.home_freq, 98)
        self.assertEqual(objs[0].vals.away_freq, 98)
        self.assertEqual(objs[0].vals.draw_freq, 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestStatistics.db.disableForeignKeys()

        TestStatistics.db.upsert(
                Statistics('statistics generation_date TD', 98, 'league name TD', 100, 100, 100, 100, 100))
        objs = TestStatistics.db.select(Statistics('statistics generation_date TD', 98, 'league name TD'))
        self.assertEqual(len(objs), 1)

        d = eval("{'mark': 100, 'mark_freq': 100, 'home_freq': 100, 'away_freq': 100, 'draw_freq': 100}")
        for k, v in d.items():
            self.assertEqual(objs[0].vals.__getattribute__(k), v)

        TestStatistics.db.rollback()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestStatistics.db.disableForeignKeys()

        TestStatistics.db.upsert(
                Statistics('statistics generation_date TD INS', 100, 'league name TD INS', 100, 100, 100, 100, 100))
        objs = TestStatistics.db.select(Statistics())
        self.assertEqual(len(objs), 3)

        d = eval("{'mark': 100, 'mark_freq': 100, 'home_freq': 100, 'away_freq': 100, 'draw_freq': 100}")
        for k, v in d.items():
            self.assertEqual(objs[2].vals.__getattribute__(k), v)

        TestStatistics.db.rollback()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestStatistics.db.disableForeignKeys()

        TestStatistics.db.delete(Statistics('statistics generation_date TD', 98, 'league name TD'))

        objs = TestStatistics.db.select(Statistics())
        self.assertEqual(len(objs), 1)

        TestStatistics.db.rollback()

if __name__ == '__main__':
    import unittest
    unittest.main()
