# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.league import League, LeagueKeys, LeagueValues
from Footy.src.database.database import Database, DatabaseKeys, AdhocKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestLeague(TestCase):
    """League object tests"""
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
        keys =LeagueKeys('league name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.name = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = League.createAdhoc(AdhocKeys('league', None))
        self.assertEqual(l.keys.table, 'league')
        self.assertTrue(l.keys.getFields() is None)

    def test_createSingle(self):
        obj = League.createSingle(('league name TD', 'league desc TD'))

        self.assertEqual(obj.keys.name, 'league name TD')
         
        self.assertEqual(obj.vals.desc, 'league desc TD')
         

    def test_createMulti(self):
        rows = [('league name TD', 'league desc TD'),
                ('league name TD2', 'league desc TD2')]
        objs = League.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.name, 'league name TD')
        
        self.assertEqual(objs[0].vals.desc, 'league desc TD')
        
        self.assertEqual(objs[1].keys.name, 'league name TD2')
        
        self.assertEqual(objs[1].vals.desc, 'league desc TD2')
        

    def test_repr(self):
        obj = League('league name TD', 'league desc TD')
        self.assertEqual(str(obj), "league : Keys {'name': 'league name TD'} : Values {'desc': 'league desc TD'}")

    def test_select(self):
        objs = TestLeague.db.select(League())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.name, 'league name TD')
        
        self.assertEqual(objs[0].vals.desc, 'league desc TD')
        
        self.assertEqual(objs[1].keys.name, 'league name TD2')
        
        self.assertEqual(objs[1].vals.desc, 'league desc TD2')
        
        
        objs = TestLeague.db.select(League('league name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.name, 'league name TD')
        
        self.assertEqual(objs[0].vals.desc, 'league desc TD')
        

        objs = TestLeague.db.select(League.createAdhoc(AdhocKeys('league', {'desc': 'league desc TD'})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.name, 'league name TD')
        
        self.assertEqual(objs[0].vals.desc, 'league desc TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestLeague.db.disableForeignKeys()

        with TestLeague.db.transaction() as t:
            TestLeague.db.upsert(
                    League('league name TD', 'league desc TD UPD'))
            objs = TestLeague.db.select(League('league name TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].keys.name, 'league name TD')
            

            d = eval("{'desc': 'league desc TD UPD'}")
            for k, v in d.items():
                self.assertEqual(objs[0].vals.__getattribute__(k), v)

            # force a rollback
            t.fail()

        with TestLeague.db.transaction() as t:
            league = TestLeague.db.select(League('league name TD'))[0]
            for k, v in d.items():
                object.__setattr__(league.vals, k, v)

            TestLeague.db.upsert(league)

            objs = TestLeague.db.select(League('league name TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].keys.name, 'league name TD')
            

            for k, v in d.items():
                self.assertEqual(objs[0].vals.__getattribute__(k), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestLeague.db.disableForeignKeys()

        with TestLeague.db.transaction() as t:
            TestLeague.db.upsert(
                    League('league name TD INS', 'league desc TD UPD'))
            objs = TestLeague.db.select(League())

            self.assertEqual(len(objs), 3)

            d = eval("{'name': 'league name TD INS'}")
            for k, v in d.items():
                self.assertEqual(objs[2].keys.__getattribute__(k), v)

            d = eval("{'desc': 'league desc TD UPD'}")
            for k, v in d.items():
                self.assertEqual(objs[2].vals.__getattribute__(k), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestLeague.db.disableForeignKeys()

        with TestLeague.db.transaction() as t:
            TestLeague.db.delete(League('league name TD'))

            objs = TestLeague.db.select(League())
            self.assertEqual(len(objs), 1)
            # force a rollback
            t.fail()

if __name__ == '__main__':
    import unittest
    unittest.main()
