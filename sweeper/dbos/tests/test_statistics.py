# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from sweeper.dbos.statistics import Statistics, StatisticsKeys, StatisticsValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestStatistics(TestCase):
    """Statistics object tests"""
    db = None

    @classmethod
    def setUpClass(cls):
        createName = 'c:/Users/Mach1/Documents/Projects/sweeper/db/createdb.sql'
        testDataName = 'c:/Users/Mach1/Documents/Projects/sweeper/db/dbos/' + '*_data.sql' 
        dbName = './db/test.db'
        os.system('cat {} | sqlite3 {}'.format(createName, dbName))
        os.system('cat {} | sqlite3 {}'.format(testDataName, dbName))
        cls.db = Database(dbName, SQLite3Impl())

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_keys_Immutablility(self):
        keys =StatisticsKeys('statistics generation_date TD', 98, 'league mnemonic TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.generation_date = 'Something New'
            keys.algo_id = 75
            keys.league = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Statistics.createAdhoc(None)
        self.assertEqual(l.getTable(), 'statistics')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Statistics.create(('statistics generation_date TD', 98, 'league mnemonic TD', 98, 98, 98, 98, 98))

        self.assertEqual(obj.getGeneration_Date(), 'statistics generation_date TD')
        self.assertEqual(obj.getAlgo_Id(), 98)
        self.assertEqual(obj.getLeague(), 'league mnemonic TD')
         
        self.assertEqual(obj.getMark(), 98)
        self.assertEqual(obj.getMark_Freq(), 98)
        self.assertEqual(obj.getHome_Freq(), 98)
        self.assertEqual(obj.getAway_Freq(), 98)
        self.assertEqual(obj.getDraw_Freq(), 98)
         

    def test_repr(self):
        obj = Statistics('statistics generation_date TD', 98, 'league mnemonic TD', 98, 98, 98, 98, 98)
        self.assertEqual(str(obj), "statistics : Keys {'generation_date': 'statistics generation_date TD', 'algo_id': 98, 'league': 'league mnemonic TD'} : Values {'mark': 98, 'mark_freq': 98, 'home_freq': 98, 'away_freq': 98, 'draw_freq': 98}")

    def test_select(self):
        objs = TestStatistics.db.select(Statistics())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getGeneration_Date(), 'statistics generation_date TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getMark(), 98)
        self.assertEqual(objs[0].getMark_Freq(), 98)
        self.assertEqual(objs[0].getHome_Freq(), 98)
        self.assertEqual(objs[0].getAway_Freq(), 98)
        self.assertEqual(objs[0].getDraw_Freq(), 98)
        
        self.assertEqual(objs[1].getGeneration_Date(), 'statistics generation_date TD2')
        self.assertEqual(objs[1].getAlgo_Id(), 99)
        self.assertEqual(objs[1].getLeague(), 'league mnemonic TD2')
        
        self.assertEqual(objs[1].getMark(), 99)
        self.assertEqual(objs[1].getMark_Freq(), 99)
        self.assertEqual(objs[1].getHome_Freq(), 99)
        self.assertEqual(objs[1].getAway_Freq(), 99)
        self.assertEqual(objs[1].getDraw_Freq(), 99)
        
        
        objs = TestStatistics.db.select(Statistics('statistics generation_date TD', 98, 'league mnemonic TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getGeneration_Date(), 'statistics generation_date TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getMark(), 98)
        self.assertEqual(objs[0].getMark_Freq(), 98)
        self.assertEqual(objs[0].getHome_Freq(), 98)
        self.assertEqual(objs[0].getAway_Freq(), 98)
        self.assertEqual(objs[0].getDraw_Freq(), 98)
        

        objs = TestStatistics.db.select(Statistics.createAdhoc({'mark': 98, 'mark_freq': 98, 'home_freq': 98, 'away_freq': 98, 'draw_freq': 98}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getGeneration_Date(), 'statistics generation_date TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getMark(), 98)
        self.assertEqual(objs[0].getMark_Freq(), 98)
        self.assertEqual(objs[0].getHome_Freq(), 98)
        self.assertEqual(objs[0].getAway_Freq(), 98)
        self.assertEqual(objs[0].getDraw_Freq(), 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestStatistics.db.disableForeignKeys()

        with TestStatistics.db.transaction() as t:
            TestStatistics.db.upsert(
                    Statistics('statistics generation_date TD', 98, 'league mnemonic TD', 100, 100, 100, 100, 100))
            objs = TestStatistics.db.select(Statistics('statistics generation_date TD', 98, 'league mnemonic TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getGeneration_Date(), 'statistics generation_date TD')
            self.assertEqual(objs[0].getAlgo_Id(), 98)
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            

            d = eval("{'mark': 100, 'mark_freq': 100, 'home_freq': 100, 'away_freq': 100, 'draw_freq': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestStatistics.db.transaction() as t:
            statistics = TestStatistics.db.select(Statistics('statistics generation_date TD', 98, 'league mnemonic TD'))[0]
            for k, v in d.items():
                statistics.__getattribute__('set' + k.title())(v)

            TestStatistics.db.upsert(statistics)

            objs = TestStatistics.db.select(Statistics('statistics generation_date TD', 98, 'league mnemonic TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getGeneration_Date(), 'statistics generation_date TD')
            self.assertEqual(objs[0].getAlgo_Id(), 98)
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestStatistics.db.disableForeignKeys()

        with TestStatistics.db.transaction() as t:
            TestStatistics.db.upsert(
                    Statistics('statistics generation_date TD INS', 100, 'league mnemonic TD INS', 100, 100, 100, 100, 100))
            objs = TestStatistics.db.select(Statistics())

            self.assertEqual(len(objs), 3)

            d = eval("{'generation_date': 'statistics generation_date TD INS', 'algo_id': 100, 'league': 'league mnemonic TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'mark': 100, 'mark_freq': 100, 'home_freq': 100, 'away_freq': 100, 'draw_freq': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestStatistics.db.disableForeignKeys()

        with TestStatistics.db.transaction() as t:
            TestStatistics.db.delete(Statistics('statistics generation_date TD', 98, 'league mnemonic TD'))

            objs = TestStatistics.db.select(Statistics())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Statistics()
        self.assertTrue(True) 

if __name__ == '__main__':
    import unittest
    unittest.main()
