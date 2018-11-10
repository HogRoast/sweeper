# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from sweeper.dbos.league import League, LeagueKeys, LeagueValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestLeague(TestCase):
    """League object tests"""
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
        keys =LeagueKeys('league mnemonic TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.mnemonic = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = League.createAdhoc(None)
        self.assertEqual(l.getTable(), 'league')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = League.create(('league mnemonic TD', 'league name TD', 'league desc TD'))

        self.assertEqual(obj.getMnemonic(), 'league mnemonic TD')
         
        self.assertEqual(obj.getName(), 'league name TD')
        self.assertEqual(obj.getDesc(), 'league desc TD')
         

    def test_repr(self):
        obj = League('league mnemonic TD', 'league name TD', 'league desc TD')
        self.assertEqual(str(obj), "league : Keys {'mnemonic': 'league mnemonic TD'} : Values {'name': 'league name TD', 'desc': 'league desc TD'}")

    def test_select(self):
        objs = TestLeague.db.select(League())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getMnemonic(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getName(), 'league name TD')
        self.assertEqual(objs[0].getDesc(), 'league desc TD')
        
        self.assertEqual(objs[1].getMnemonic(), 'league mnemonic TD2')
        
        self.assertEqual(objs[1].getName(), 'league name TD2')
        self.assertEqual(objs[1].getDesc(), 'league desc TD2')
        
        
        objs = TestLeague.db.select(League('league mnemonic TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getMnemonic(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getName(), 'league name TD')
        self.assertEqual(objs[0].getDesc(), 'league desc TD')
        

        objs = TestLeague.db.select(League.createAdhoc({'name': 'league name TD', 'desc': 'league desc TD'}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getMnemonic(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getName(), 'league name TD')
        self.assertEqual(objs[0].getDesc(), 'league desc TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestLeague.db.disableForeignKeys()

        with TestLeague.db.transaction() as t:
            TestLeague.db.upsert(
                    League('league mnemonic TD', 'league name TD UPD', 'league desc TD UPD'))
            objs = TestLeague.db.select(League('league mnemonic TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getMnemonic(), 'league mnemonic TD')
            

            d = eval("{'name': 'league name TD UPD', 'desc': 'league desc TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestLeague.db.transaction() as t:
            league = TestLeague.db.select(League('league mnemonic TD'))[0]
            for k, v in d.items():
                league.__getattribute__('set' + k.title())(v)

            TestLeague.db.upsert(league)

            objs = TestLeague.db.select(League('league mnemonic TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getMnemonic(), 'league mnemonic TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestLeague.db.disableForeignKeys()

        with TestLeague.db.transaction() as t:
            TestLeague.db.upsert(
                    League('league mnemonic TD INS', 'league name TD UPD', 'league desc TD UPD'))
            objs = TestLeague.db.select(League())

            self.assertEqual(len(objs), 3)

            d = eval("{'mnemonic': 'league mnemonic TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'name': 'league name TD UPD', 'desc': 'league desc TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestLeague.db.disableForeignKeys()

        with TestLeague.db.transaction() as t:
            TestLeague.db.delete(League('league mnemonic TD'))

            objs = TestLeague.db.select(League())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = League()
        self.assertTrue(True and obj.isNullable('desc')) 

if __name__ == '__main__':
    import unittest
    unittest.main()
