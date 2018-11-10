# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from sweeper.dbos.source_league_map import Source_League_Map, Source_League_MapKeys, Source_League_MapValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestSource_League_Map(TestCase):
    """Source_League_Map object tests"""
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
        keys =Source_League_MapKeys(98, 'league mnemonic TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.source_id = 75
            keys.league = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Source_League_Map.createAdhoc(None)
        self.assertEqual(l.getTable(), 'source_league_map')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Source_League_Map.create((98, 'league mnemonic TD', 'source_league_map moniker TD'))

        self.assertEqual(obj.getSource_Id(), 98)
        self.assertEqual(obj.getLeague(), 'league mnemonic TD')
         
        self.assertEqual(obj.getMoniker(), 'source_league_map moniker TD')
         

    def test_repr(self):
        obj = Source_League_Map(98, 'league mnemonic TD', 'source_league_map moniker TD')
        self.assertEqual(str(obj), "source_league_map : Keys {'source_id': 98, 'league': 'league mnemonic TD'} : Values {'moniker': 'source_league_map moniker TD'}")

    def test_select(self):
        objs = TestSource_League_Map.db.select(Source_League_Map())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_league_map moniker TD')
        
        self.assertEqual(objs[1].getSource_Id(), 99)
        self.assertEqual(objs[1].getLeague(), 'league mnemonic TD2')
        
        self.assertEqual(objs[1].getMoniker(), 'source_league_map moniker TD2')
        
        
        objs = TestSource_League_Map.db.select(Source_League_Map(98, 'league mnemonic TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_league_map moniker TD')
        

        objs = TestSource_League_Map.db.select(Source_League_Map.createAdhoc({'moniker': 'source_league_map moniker TD'}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_league_map moniker TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestSource_League_Map.db.disableForeignKeys()

        with TestSource_League_Map.db.transaction() as t:
            TestSource_League_Map.db.upsert(
                    Source_League_Map(98, 'league mnemonic TD', 'source_league_map moniker TD UPD'))
            objs = TestSource_League_Map.db.select(Source_League_Map(98, 'league mnemonic TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getSource_Id(), 98)
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            

            d = eval("{'moniker': 'source_league_map moniker TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestSource_League_Map.db.transaction() as t:
            source_league_map = TestSource_League_Map.db.select(Source_League_Map(98, 'league mnemonic TD'))[0]
            for k, v in d.items():
                source_league_map.__getattribute__('set' + k.title())(v)

            TestSource_League_Map.db.upsert(source_league_map)

            objs = TestSource_League_Map.db.select(Source_League_Map(98, 'league mnemonic TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getSource_Id(), 98)
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestSource_League_Map.db.disableForeignKeys()

        with TestSource_League_Map.db.transaction() as t:
            TestSource_League_Map.db.upsert(
                    Source_League_Map(100, 'league mnemonic TD INS', 'source_league_map moniker TD UPD'))
            objs = TestSource_League_Map.db.select(Source_League_Map())

            self.assertEqual(len(objs), 3)

            d = eval("{'source_id': 100, 'league': 'league mnemonic TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'moniker': 'source_league_map moniker TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestSource_League_Map.db.disableForeignKeys()

        with TestSource_League_Map.db.transaction() as t:
            TestSource_League_Map.db.delete(Source_League_Map(98, 'league mnemonic TD'))

            objs = TestSource_League_Map.db.select(Source_League_Map())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Source_League_Map()
        self.assertTrue(True and obj.isNullable('league') and obj.isNullable('moniker')) 

if __name__ == '__main__':
    import unittest
    unittest.main()
