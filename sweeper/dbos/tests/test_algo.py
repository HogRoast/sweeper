# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from sweeper.dbos.algo import Algo, AlgoKeys, AlgoValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestAlgo(TestCase):
    """Algo object tests"""
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
        keys =AlgoKeys(98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Algo.createAdhoc(None)
        self.assertEqual(l.getTable(), 'algo')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Algo.create((98, 'algo name TD', 'algo desc TD'))

        self.assertEqual(obj.getId(), 98)
         
        self.assertEqual(obj.getName(), 'algo name TD')
        self.assertEqual(obj.getDesc(), 'algo desc TD')
         

    def test_repr(self):
        obj = Algo(98, 'algo name TD', 'algo desc TD')
        self.assertEqual(str(obj), "algo : Keys {'id': 98} : Values {'name': 'algo name TD', 'desc': 'algo desc TD'}")

    def test_select(self):
        objs = TestAlgo.db.select(Algo())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'algo name TD')
        self.assertEqual(objs[0].getDesc(), 'algo desc TD')
        
        self.assertEqual(objs[1].getId(), 99)
        
        self.assertEqual(objs[1].getName(), 'algo name TD2')
        self.assertEqual(objs[1].getDesc(), 'algo desc TD2')
        
        
        objs = TestAlgo.db.select(Algo(98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'algo name TD')
        self.assertEqual(objs[0].getDesc(), 'algo desc TD')
        

        objs = TestAlgo.db.select(Algo.createAdhoc({'name': 'algo name TD', 'desc': 'algo desc TD'}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'algo name TD')
        self.assertEqual(objs[0].getDesc(), 'algo desc TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestAlgo.db.disableForeignKeys()

        with TestAlgo.db.transaction() as t:
            TestAlgo.db.upsert(
                    Algo(98, 'algo name TD UPD', 'algo desc TD UPD'))
            objs = TestAlgo.db.select(Algo(98))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            d = eval("{'name': 'algo name TD UPD', 'desc': 'algo desc TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestAlgo.db.transaction() as t:
            algo = TestAlgo.db.select(Algo(98))[0]
            for k, v in d.items():
                algo.__getattribute__('set' + k.title())(v)

            TestAlgo.db.upsert(algo)

            objs = TestAlgo.db.select(Algo(98))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestAlgo.db.disableForeignKeys()

        with TestAlgo.db.transaction() as t:
            TestAlgo.db.upsert(
                    Algo(100, 'algo name TD UPD', 'algo desc TD UPD'))
            objs = TestAlgo.db.select(Algo())

            self.assertEqual(len(objs), 3)

            d = eval("{'id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'name': 'algo name TD UPD', 'desc': 'algo desc TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestAlgo.db.disableForeignKeys()

        with TestAlgo.db.transaction() as t:
            TestAlgo.db.delete(Algo(98))

            objs = TestAlgo.db.select(Algo())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Algo()
        self.assertTrue(True and obj.isNullable('name') and obj.isNullable('desc')) 

if __name__ == '__main__':
    import unittest
    unittest.main()
