# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.source_season_map import Source_Season_Map, Source_Season_MapKeys, Source_Season_MapValues
from Footy.src.database.database import Database, AdhocKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestSource_Season_Map(TestCase):
    """Source_Season_Map object tests"""
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
        pass

    def tearDown(self):
        pass

    def test_keys_Immutablility(self):
        keys =Source_Season_MapKeys(98, 'season name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.source_id = 75
            keys.season = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Source_Season_Map.createAdhoc(AdhocKeys(None))
        self.assertEqual(l.getTable(), 'source_season_map')
        self.assertTrue(l._keys.getFields() is None)

    def test_createSingle(self):
        obj = Source_Season_Map.createSingle((98, 'season name TD', 'source_season_map moniker TD', 'source_season_map data_url TD'))

        self.assertEqual(obj.getSource_Id(), 98)
        self.assertEqual(obj.getSeason(), 'season name TD')
         
        self.assertEqual(obj.getMoniker(), 'source_season_map moniker TD')
        self.assertEqual(obj.getData_Url(), 'source_season_map data_url TD')
         

    def test_createMulti(self):
        rows = [(98, 'season name TD', 'source_season_map moniker TD', 'source_season_map data_url TD'),
                (99, 'season name TD2', 'source_season_map moniker TD2', 'source_season_map data_url TD2')]
        objs = Source_Season_Map.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getSeason(), 'season name TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_season_map moniker TD')
        self.assertEqual(objs[0].getData_Url(), 'source_season_map data_url TD')
        
        self.assertEqual(objs[1].getSource_Id(), 99)
        self.assertEqual(objs[1].getSeason(), 'season name TD2')
        
        self.assertEqual(objs[1].getMoniker(), 'source_season_map moniker TD2')
        self.assertEqual(objs[1].getData_Url(), 'source_season_map data_url TD2')
        

    def test_repr(self):
        obj = Source_Season_Map(98, 'season name TD', 'source_season_map moniker TD', 'source_season_map data_url TD')
        self.assertEqual(str(obj), "source_season_map : Keys {'source_id': 98, 'season': 'season name TD'} : Values {'moniker': 'source_season_map moniker TD', 'data_url': 'source_season_map data_url TD'}")

    def test_select(self):
        objs = TestSource_Season_Map.db.select(Source_Season_Map())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getSeason(), 'season name TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_season_map moniker TD')
        self.assertEqual(objs[0].getData_Url(), 'source_season_map data_url TD')
        
        self.assertEqual(objs[1].getSource_Id(), 99)
        self.assertEqual(objs[1].getSeason(), 'season name TD2')
        
        self.assertEqual(objs[1].getMoniker(), 'source_season_map moniker TD2')
        self.assertEqual(objs[1].getData_Url(), 'source_season_map data_url TD2')
        
        
        objs = TestSource_Season_Map.db.select(Source_Season_Map(98, 'season name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getSeason(), 'season name TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_season_map moniker TD')
        self.assertEqual(objs[0].getData_Url(), 'source_season_map data_url TD')
        

        objs = TestSource_Season_Map.db.select(Source_Season_Map.createAdhoc(AdhocKeys({'moniker': 'source_season_map moniker TD', 'data_url': 'source_season_map data_url TD'})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getSeason(), 'season name TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_season_map moniker TD')
        self.assertEqual(objs[0].getData_Url(), 'source_season_map data_url TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestSource_Season_Map.db.disableForeignKeys()

        with TestSource_Season_Map.db.transaction() as t:
            TestSource_Season_Map.db.upsert(
                    Source_Season_Map(98, 'season name TD', 'source_season_map moniker TD UPD', 'source_season_map data_url TD UPD'))
            objs = TestSource_Season_Map.db.select(Source_Season_Map(98, 'season name TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getSource_Id(), 98)
            self.assertEqual(objs[0].getSeason(), 'season name TD')
            

            d = eval("{'moniker': 'source_season_map moniker TD UPD', 'data_url': 'source_season_map data_url TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestSource_Season_Map.db.transaction() as t:
            source_season_map = TestSource_Season_Map.db.select(Source_Season_Map(98, 'season name TD'))[0]
            for k, v in d.items():
                source_season_map.__getattribute__('set' + k.title())(v)

            TestSource_Season_Map.db.upsert(source_season_map)

            objs = TestSource_Season_Map.db.select(Source_Season_Map(98, 'season name TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getSource_Id(), 98)
            self.assertEqual(objs[0].getSeason(), 'season name TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestSource_Season_Map.db.disableForeignKeys()

        with TestSource_Season_Map.db.transaction() as t:
            TestSource_Season_Map.db.upsert(
                    Source_Season_Map(100, 'season name TD INS', 'source_season_map moniker TD UPD', 'source_season_map data_url TD UPD'))
            objs = TestSource_Season_Map.db.select(Source_Season_Map())

            self.assertEqual(len(objs), 3)

            d = eval("{'source_id': 100, 'season': 'season name TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'moniker': 'source_season_map moniker TD UPD', 'data_url': 'source_season_map data_url TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestSource_Season_Map.db.disableForeignKeys()

        with TestSource_Season_Map.db.transaction() as t:
            TestSource_Season_Map.db.delete(Source_Season_Map(98, 'season name TD'))

            objs = TestSource_Season_Map.db.select(Source_Season_Map())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

if __name__ == '__main__':
    import unittest
    unittest.main()
