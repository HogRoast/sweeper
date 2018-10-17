# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.plan import Plan, PlanKeys, PlanValues
from Footy.src.database.database import Database, DatabaseKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestPlan(TestCase):
    """Plan object tests"""
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
        keys =PlanKeys(98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Plan.createAdhoc(DatabaseKeys('plan', None))
        self.assertEqual(l.keys.table, 'plan')
        self.assertTrue(l.keys.fields is None)

    def test_createSingle(self):
        obj = Plan.createSingle((98, 'plan name TD', 'plan desc TD', 2.3))

        self.assertEqual(obj.keys.id, 98)
         
        self.assertEqual(obj.vals.name, 'plan name TD')
        self.assertEqual(obj.vals.desc, 'plan desc TD')
        self.assertEqual(obj.vals.cost, 2.3)
         

    def test_createMulti(self):
        rows = [(98, 'plan name TD', 'plan desc TD', 2.3),
                (99, 'plan name TD2', 'plan desc TD2', 2.4)]
        objs = Plan.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.name, 'plan name TD')
        self.assertEqual(objs[0].vals.desc, 'plan desc TD')
        self.assertEqual(objs[0].vals.cost, 2.3)
        
        self.assertEqual(objs[1].keys.id, 99)
        
        self.assertEqual(objs[1].vals.name, 'plan name TD2')
        self.assertEqual(objs[1].vals.desc, 'plan desc TD2')
        self.assertEqual(objs[1].vals.cost, 2.4)
        

    def test_repr(self):
        obj = Plan(98, 'plan name TD', 'plan desc TD', 2.3)
        self.assertEqual(str(obj), "plan : Keys {'id': 98} : Values {'name': 'plan name TD', 'desc': 'plan desc TD', 'cost': 2.3}")

    def test_select(self):
        objs = TestPlan.db.select(Plan())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.name, 'plan name TD')
        self.assertEqual(objs[0].vals.desc, 'plan desc TD')
        self.assertEqual(objs[0].vals.cost, 2.3)
        
        self.assertEqual(objs[1].keys.id, 99)
        
        self.assertEqual(objs[1].vals.name, 'plan name TD2')
        self.assertEqual(objs[1].vals.desc, 'plan desc TD2')
        self.assertEqual(objs[1].vals.cost, 2.4)
        
        
        objs = TestPlan.db.select(Plan(98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.name, 'plan name TD')
        self.assertEqual(objs[0].vals.desc, 'plan desc TD')
        self.assertEqual(objs[0].vals.cost, 2.3)
        

        objs = TestPlan.db.select(Plan.createAdhoc(DatabaseKeys('plan', {'name': 'plan name TD', 'desc': 'plan desc TD', 'cost': 2.3})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.name, 'plan name TD')
        self.assertEqual(objs[0].vals.desc, 'plan desc TD')
        self.assertEqual(objs[0].vals.cost, 2.3)
        

if __name__ == '__main__':
    import unittest
    unittest.main()
