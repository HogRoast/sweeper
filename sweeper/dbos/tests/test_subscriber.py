# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from sweeper.dbos.subscriber import Subscriber, SubscriberKeys, SubscriberValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestSubscriber(TestCase):
    """Subscriber object tests"""
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
        keys =SubscriberKeys('subscriber email TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.email = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Subscriber.createAdhoc(None)
        self.assertEqual(l.getTable(), 'subscriber')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Subscriber.create(('subscriber email TD', 98, 'subscriber first_name TD', 'subscriber second_name TD'))

        self.assertEqual(obj.getEmail(), 'subscriber email TD')
         
        self.assertEqual(obj.getInclude(), 98)
        self.assertEqual(obj.getFirst_Name(), 'subscriber first_name TD')
        self.assertEqual(obj.getSecond_Name(), 'subscriber second_name TD')
         

    def test_repr(self):
        obj = Subscriber('subscriber email TD', 98, 'subscriber first_name TD', 'subscriber second_name TD')
        self.assertEqual(str(obj), "subscriber : Keys {'email': 'subscriber email TD'} : Values {'include': 98, 'first_name': 'subscriber first_name TD', 'second_name': 'subscriber second_name TD'}")

    def test_select(self):
        objs = TestSubscriber.db.select(Subscriber())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getEmail(), 'subscriber email TD')
        
        self.assertEqual(objs[0].getInclude(), 98)
        self.assertEqual(objs[0].getFirst_Name(), 'subscriber first_name TD')
        self.assertEqual(objs[0].getSecond_Name(), 'subscriber second_name TD')
        
        self.assertEqual(objs[1].getEmail(), 'subscriber email TD2')
        
        self.assertEqual(objs[1].getInclude(), 99)
        self.assertEqual(objs[1].getFirst_Name(), 'subscriber first_name TD2')
        self.assertEqual(objs[1].getSecond_Name(), 'subscriber second_name TD2')
        
        
        objs = TestSubscriber.db.select(Subscriber('subscriber email TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getEmail(), 'subscriber email TD')
        
        self.assertEqual(objs[0].getInclude(), 98)
        self.assertEqual(objs[0].getFirst_Name(), 'subscriber first_name TD')
        self.assertEqual(objs[0].getSecond_Name(), 'subscriber second_name TD')
        

        objs = TestSubscriber.db.select(Subscriber.createAdhoc({'include': 98, 'first_name': 'subscriber first_name TD', 'second_name': 'subscriber second_name TD'}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getEmail(), 'subscriber email TD')
        
        self.assertEqual(objs[0].getInclude(), 98)
        self.assertEqual(objs[0].getFirst_Name(), 'subscriber first_name TD')
        self.assertEqual(objs[0].getSecond_Name(), 'subscriber second_name TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestSubscriber.db.disableForeignKeys()

        with TestSubscriber.db.transaction() as t:
            TestSubscriber.db.upsert(
                    Subscriber('subscriber email TD', 100, 'subscriber first_name TD UPD', 'subscriber second_name TD UPD'))
            objs = TestSubscriber.db.select(Subscriber('subscriber email TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getEmail(), 'subscriber email TD')
            

            d = eval("{'include': 100, 'first_name': 'subscriber first_name TD UPD', 'second_name': 'subscriber second_name TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestSubscriber.db.transaction() as t:
            subscriber = TestSubscriber.db.select(Subscriber('subscriber email TD'))[0]
            for k, v in d.items():
                subscriber.__getattribute__('set' + k.title())(v)

            TestSubscriber.db.upsert(subscriber)

            objs = TestSubscriber.db.select(Subscriber('subscriber email TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getEmail(), 'subscriber email TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestSubscriber.db.disableForeignKeys()

        with TestSubscriber.db.transaction() as t:
            TestSubscriber.db.upsert(
                    Subscriber('subscriber email TD INS', 100, 'subscriber first_name TD UPD', 'subscriber second_name TD UPD'))
            objs = TestSubscriber.db.select(Subscriber())

            self.assertEqual(len(objs), 3)

            d = eval("{'email': 'subscriber email TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'include': 100, 'first_name': 'subscriber first_name TD UPD', 'second_name': 'subscriber second_name TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestSubscriber.db.disableForeignKeys()

        with TestSubscriber.db.transaction() as t:
            TestSubscriber.db.delete(Subscriber('subscriber email TD'))

            objs = TestSubscriber.db.select(Subscriber())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Subscriber()
        self.assertTrue(True and obj.isNullable('first_name') and obj.isNullable('second_name')) 

if __name__ == '__main__':
    import unittest
    unittest.main()
