# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.plan import Plan, PlanKeys, PlanValues
from Footy.src.database.database import Database, AdhocKeys
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
        l = Plan.createAdhoc(AdhocKeys(None))
        self.assertEqual(l.getTable(), 'plan')
        self.assertTrue(l._keys.getFields() is None)

    def test_createSingle(self):
        obj = Plan.createSingle((98, 'plan name TD', 2.3, 'plan desc TD'))

        self.assertEqual(obj.getId(), 98)
         
        self.assertEqual(obj.getName(), 'plan name TD')
        self.assertEqual(obj.getCost(), 2.3)
        self.assertEqual(obj.getDesc(), 'plan desc TD')
         

    def test_createMulti(self):
        rows = [(98, 'plan name TD', 2.3, 'plan desc TD'),
                (99, 'plan name TD2', 2.4, 'plan desc TD2')]
        objs = Plan.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'plan name TD')
        self.assertEqual(objs[0].getCost(), 2.3)
        self.assertEqual(objs[0].getDesc(), 'plan desc TD')
        
        self.assertEqual(objs[1].getId(), 99)
        
        self.assertEqual(objs[1].getName(), 'plan name TD2')
        self.assertEqual(objs[1].getCost(), 2.4)
        self.assertEqual(objs[1].getDesc(), 'plan desc TD2')
        

    def test_repr(self):
        obj = Plan(98, 'plan name TD', 2.3, 'plan desc TD')
        self.assertEqual(str(obj), "plan : Keys {'id': 98} : Values {'name': 'plan name TD', 'cost': 2.3, 'desc': 'plan desc TD'}")

    def test_select(self):
        objs = TestPlan.db.select(Plan())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'plan name TD')
        self.assertEqual(objs[0].getCost(), 2.3)
        self.assertEqual(objs[0].getDesc(), 'plan desc TD')
        
        self.assertEqual(objs[1].getId(), 99)
        
        self.assertEqual(objs[1].getName(), 'plan name TD2')
        self.assertEqual(objs[1].getCost(), 2.4)
        self.assertEqual(objs[1].getDesc(), 'plan desc TD2')
        
        
        objs = TestPlan.db.select(Plan(98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'plan name TD')
        self.assertEqual(objs[0].getCost(), 2.3)
        self.assertEqual(objs[0].getDesc(), 'plan desc TD')
        

        objs = TestPlan.db.select(Plan.createAdhoc(AdhocKeys({'name': 'plan name TD', 'cost': 2.3, 'desc': 'plan desc TD'})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'plan name TD')
        self.assertEqual(objs[0].getCost(), 2.3)
        self.assertEqual(objs[0].getDesc(), 'plan desc TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestPlan.db.disableForeignKeys()

        with TestPlan.db.transaction() as t:
            TestPlan.db.upsert(
                    Plan(98, 'plan name TD UPD', 5.6, 'plan desc TD UPD'))
            objs = TestPlan.db.select(Plan(98))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            d = eval("{'name': 'plan name TD UPD', 'cost': 5.6, 'desc': 'plan desc TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestPlan.db.transaction() as t:
            plan = TestPlan.db.select(Plan(98))[0]
            for k, v in d.items():
                plan.__getattribute__('set' + k.title())(v)

            TestPlan.db.upsert(plan)

            objs = TestPlan.db.select(Plan(98))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestPlan.db.disableForeignKeys()

        with TestPlan.db.transaction() as t:
            TestPlan.db.upsert(
                    Plan(100, 'plan name TD UPD', 5.6, 'plan desc TD UPD'))
            objs = TestPlan.db.select(Plan())

            self.assertEqual(len(objs), 3)

            d = eval("{'id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'name': 'plan name TD UPD', 'cost': 5.6, 'desc': 'plan desc TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestPlan.db.disableForeignKeys()

        with TestPlan.db.transaction() as t:
            TestPlan.db.delete(Plan(98))

            objs = TestPlan.db.select(Plan())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Plan()
        self.assertTrue(True and obj.isNullable('desc')) 

if __name__ == '__main__':
    import unittest
    unittest.main()
