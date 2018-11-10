# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from sweeper.dbos.source_team_map import Source_Team_Map, Source_Team_MapKeys, Source_Team_MapValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestSource_Team_Map(TestCase):
    """Source_Team_Map object tests"""
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
        keys =Source_Team_MapKeys(98, 'source_team_map moniker TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.source_id = 75
            keys.moniker = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Source_Team_Map.createAdhoc(None)
        self.assertEqual(l.getTable(), 'source_team_map')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Source_Team_Map.create((98, 'source_team_map moniker TD', 'team name TD'))

        self.assertEqual(obj.getSource_Id(), 98)
        self.assertEqual(obj.getMoniker(), 'source_team_map moniker TD')
         
        self.assertEqual(obj.getTeam(), 'team name TD')
         

    def test_repr(self):
        obj = Source_Team_Map(98, 'source_team_map moniker TD', 'team name TD')
        self.assertEqual(str(obj), "source_team_map : Keys {'source_id': 98, 'moniker': 'source_team_map moniker TD'} : Values {'team': 'team name TD'}")

    def test_select(self):
        objs = TestSource_Team_Map.db.select(Source_Team_Map())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getMoniker(), 'source_team_map moniker TD')
        
        self.assertEqual(objs[0].getTeam(), 'team name TD')
        
        self.assertEqual(objs[1].getSource_Id(), 99)
        self.assertEqual(objs[1].getMoniker(), 'source_team_map moniker TD2')
        
        self.assertEqual(objs[1].getTeam(), 'team name TD2')
        
        
        objs = TestSource_Team_Map.db.select(Source_Team_Map(98, 'source_team_map moniker TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getMoniker(), 'source_team_map moniker TD')
        
        self.assertEqual(objs[0].getTeam(), 'team name TD')
        

        objs = TestSource_Team_Map.db.select(Source_Team_Map.createAdhoc({'team': 'team name TD'}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getMoniker(), 'source_team_map moniker TD')
        
        self.assertEqual(objs[0].getTeam(), 'team name TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestSource_Team_Map.db.disableForeignKeys()

        with TestSource_Team_Map.db.transaction() as t:
            TestSource_Team_Map.db.upsert(
                    Source_Team_Map(98, 'source_team_map moniker TD', 'team name TD UPD'))
            objs = TestSource_Team_Map.db.select(Source_Team_Map(98, 'source_team_map moniker TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getSource_Id(), 98)
            self.assertEqual(objs[0].getMoniker(), 'source_team_map moniker TD')
            

            d = eval("{'team': 'team name TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestSource_Team_Map.db.transaction() as t:
            source_team_map = TestSource_Team_Map.db.select(Source_Team_Map(98, 'source_team_map moniker TD'))[0]
            for k, v in d.items():
                source_team_map.__getattribute__('set' + k.title())(v)

            TestSource_Team_Map.db.upsert(source_team_map)

            objs = TestSource_Team_Map.db.select(Source_Team_Map(98, 'source_team_map moniker TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getSource_Id(), 98)
            self.assertEqual(objs[0].getMoniker(), 'source_team_map moniker TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestSource_Team_Map.db.disableForeignKeys()

        with TestSource_Team_Map.db.transaction() as t:
            TestSource_Team_Map.db.upsert(
                    Source_Team_Map(100, 'source_team_map moniker TD INS', 'team name TD UPD'))
            objs = TestSource_Team_Map.db.select(Source_Team_Map())

            self.assertEqual(len(objs), 3)

            d = eval("{'source_id': 100, 'moniker': 'source_team_map moniker TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'team': 'team name TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestSource_Team_Map.db.disableForeignKeys()

        with TestSource_Team_Map.db.transaction() as t:
            TestSource_Team_Map.db.delete(Source_Team_Map(98, 'source_team_map moniker TD'))

            objs = TestSource_Team_Map.db.select(Source_Team_Map())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Source_Team_Map()
        self.assertTrue(True) 

if __name__ == '__main__':
    import unittest
    unittest.main()
