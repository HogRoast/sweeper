# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.source_team_map import Source_Team_Map, Source_Team_MapKeys, Source_Team_MapValues
from Footy.src.database.database import Database, AdhocKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestSource_Team_Map(TestCase):
    """Source_Team_Map object tests"""
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
        keys =Source_Team_MapKeys(98, 'team name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.source_id = 75
            keys.team = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Source_Team_Map.createAdhoc(AdhocKeys(None))
        self.assertEqual(l.getTable(), 'source_team_map')
        self.assertTrue(l._keys.getFields() is None)

    def test_createSingle(self):
        obj = Source_Team_Map.createSingle((98, 'team name TD', 'source_team_map moniker TD'))

        self.assertEqual(obj.getSource_Id(), 98)
        self.assertEqual(obj.getTeam(), 'team name TD')
         
        self.assertEqual(obj.getMoniker(), 'source_team_map moniker TD')
         

    def test_createMulti(self):
        rows = [(98, 'team name TD', 'source_team_map moniker TD'),
                (99, 'team name TD2', 'source_team_map moniker TD2')]
        objs = Source_Team_Map.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getTeam(), 'team name TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_team_map moniker TD')
        
        self.assertEqual(objs[1].getSource_Id(), 99)
        self.assertEqual(objs[1].getTeam(), 'team name TD2')
        
        self.assertEqual(objs[1].getMoniker(), 'source_team_map moniker TD2')
        

    def test_repr(self):
        obj = Source_Team_Map(98, 'team name TD', 'source_team_map moniker TD')
        self.assertEqual(str(obj), "source_team_map : Keys {'source_id': 98, 'team': 'team name TD'} : Values {'moniker': 'source_team_map moniker TD'}")

    def test_select(self):
        objs = TestSource_Team_Map.db.select(Source_Team_Map())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getTeam(), 'team name TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_team_map moniker TD')
        
        self.assertEqual(objs[1].getSource_Id(), 99)
        self.assertEqual(objs[1].getTeam(), 'team name TD2')
        
        self.assertEqual(objs[1].getMoniker(), 'source_team_map moniker TD2')
        
        
        objs = TestSource_Team_Map.db.select(Source_Team_Map(98, 'team name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getTeam(), 'team name TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_team_map moniker TD')
        

        objs = TestSource_Team_Map.db.select(Source_Team_Map.createAdhoc(AdhocKeys({'moniker': 'source_team_map moniker TD'})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getSource_Id(), 98)
        self.assertEqual(objs[0].getTeam(), 'team name TD')
        
        self.assertEqual(objs[0].getMoniker(), 'source_team_map moniker TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestSource_Team_Map.db.disableForeignKeys()

        with TestSource_Team_Map.db.transaction() as t:
            TestSource_Team_Map.db.upsert(
                    Source_Team_Map(98, 'team name TD', 'source_team_map moniker TD UPD'))
            objs = TestSource_Team_Map.db.select(Source_Team_Map(98, 'team name TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getSource_Id(), 98)
            self.assertEqual(objs[0].getTeam(), 'team name TD')
            

            d = eval("{'moniker': 'source_team_map moniker TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestSource_Team_Map.db.transaction() as t:
            source_team_map = TestSource_Team_Map.db.select(Source_Team_Map(98, 'team name TD'))[0]
            for k, v in d.items():
                source_team_map.__getattribute__('set' + k.title())(v)

            TestSource_Team_Map.db.upsert(source_team_map)

            objs = TestSource_Team_Map.db.select(Source_Team_Map(98, 'team name TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getSource_Id(), 98)
            self.assertEqual(objs[0].getTeam(), 'team name TD')
            

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
                    Source_Team_Map(100, 'team name TD INS', 'source_team_map moniker TD UPD'))
            objs = TestSource_Team_Map.db.select(Source_Team_Map())

            self.assertEqual(len(objs), 3)

            d = eval("{'source_id': 100, 'team': 'team name TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'moniker': 'source_team_map moniker TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestSource_Team_Map.db.disableForeignKeys()

        with TestSource_Team_Map.db.transaction() as t:
            TestSource_Team_Map.db.delete(Source_Team_Map(98, 'team name TD'))

            objs = TestSource_Team_Map.db.select(Source_Team_Map())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

if __name__ == '__main__':
    import unittest
    unittest.main()
