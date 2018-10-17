# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.algo import Algo, AlgoKeys, AlgoValues
from Footy.src.database.database import Database, DatabaseKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestAlgo(TestCase):
    """Algo object tests"""
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
        keys =AlgoKeys(98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Algo.createAdhoc(DatabaseKeys('algo', None))
        self.assertEqual(l.keys.table, 'algo')
        self.assertTrue(l.keys.fields is None)

    def test_createSingle(self):
        obj = Algo.createSingle((98, 'algo name TD', 'algo desc TD'))

        self.assertEqual(obj.keys.id, 98)
         
        self.assertEqual(obj.vals.name, 'algo name TD')
        self.assertEqual(obj.vals.desc, 'algo desc TD')
         

    def test_createMulti(self):
        rows = [(98, 'algo name TD', 'algo desc TD'),
                (99, 'algo name TD2', 'algo desc TD2')]
        objs = Algo.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.name, 'algo name TD')
        self.assertEqual(objs[0].vals.desc, 'algo desc TD')
        
        self.assertEqual(objs[1].keys.id, 99)
        
        self.assertEqual(objs[1].vals.name, 'algo name TD2')
        self.assertEqual(objs[1].vals.desc, 'algo desc TD2')
        

    def test_repr(self):
        obj = Algo(98, 'algo name TD', 'algo desc TD')
        self.assertEqual(str(obj), "algo : Keys {'id': 98} : Values {'name': 'algo name TD', 'desc': 'algo desc TD'}")

    def test_select(self):
        objs = TestAlgo.db.select(Algo())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.name, 'algo name TD')
        self.assertEqual(objs[0].vals.desc, 'algo desc TD')
        
        self.assertEqual(objs[1].keys.id, 99)
        
        self.assertEqual(objs[1].vals.name, 'algo name TD2')
        self.assertEqual(objs[1].vals.desc, 'algo desc TD2')
        
        
        objs = TestAlgo.db.select(Algo(98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.name, 'algo name TD')
        self.assertEqual(objs[0].vals.desc, 'algo desc TD')
        

        objs = TestAlgo.db.select(Algo.createAdhoc(DatabaseKeys('algo', {'name': 'algo name TD', 'desc': 'algo desc TD'})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.name, 'algo name TD')
        self.assertEqual(objs[0].vals.desc, 'algo desc TD')
        

if __name__ == '__main__':
    import unittest
    unittest.main()
