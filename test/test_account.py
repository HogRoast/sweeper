# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.account import Account, AccountKeys, AccountValues
from Footy.src.database.database import Database, DatabaseKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestAccount(TestCase):
    """Account object tests"""
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
        keys =AccountKeys('account name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.name = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Account.createAdhoc(DatabaseKeys('account', None))
        self.assertEqual(l.keys.table, 'account')
        self.assertTrue(l.keys.fields is None)

    def test_createSingle(self):
        obj = Account.createSingle(('account name TD', 'account expiry_date TD', 'account joined_date TD', 98))

        self.assertEqual(obj.keys.name, 'account name TD')
         
        self.assertEqual(obj.vals.expiry_date, 'account expiry_date TD')
        self.assertEqual(obj.vals.joined_date, 'account joined_date TD')
        self.assertEqual(obj.vals.plan_id, 98)
         

    def test_createMulti(self):
        rows = [('account name TD', 'account expiry_date TD', 'account joined_date TD', 98),
                ('account name TD2', 'account expiry_date TD2', 'account joined_date TD2', 99)]
        objs = Account.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.name, 'account name TD')
        
        self.assertEqual(objs[0].vals.expiry_date, 'account expiry_date TD')
        self.assertEqual(objs[0].vals.joined_date, 'account joined_date TD')
        self.assertEqual(objs[0].vals.plan_id, 98)
        
        self.assertEqual(objs[1].keys.name, 'account name TD2')
        
        self.assertEqual(objs[1].vals.expiry_date, 'account expiry_date TD2')
        self.assertEqual(objs[1].vals.joined_date, 'account joined_date TD2')
        self.assertEqual(objs[1].vals.plan_id, 99)
        

    def test_repr(self):
        obj = Account('account name TD', 'account expiry_date TD', 'account joined_date TD', 98)
        self.assertEqual(str(obj), "account : Keys {'name': 'account name TD'} : Values {'expiry_date': 'account expiry_date TD', 'joined_date': 'account joined_date TD', 'plan_id': 98}")

    def test_select(self):
        objs = TestAccount.db.select(Account())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.name, 'account name TD')
        
        self.assertEqual(objs[0].vals.expiry_date, 'account expiry_date TD')
        self.assertEqual(objs[0].vals.joined_date, 'account joined_date TD')
        self.assertEqual(objs[0].vals.plan_id, 98)
        
        self.assertEqual(objs[1].keys.name, 'account name TD2')
        
        self.assertEqual(objs[1].vals.expiry_date, 'account expiry_date TD2')
        self.assertEqual(objs[1].vals.joined_date, 'account joined_date TD2')
        self.assertEqual(objs[1].vals.plan_id, 99)
        
        
        objs = TestAccount.db.select(Account('account name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.name, 'account name TD')
        
        self.assertEqual(objs[0].vals.expiry_date, 'account expiry_date TD')
        self.assertEqual(objs[0].vals.joined_date, 'account joined_date TD')
        self.assertEqual(objs[0].vals.plan_id, 98)
        

        objs = TestAccount.db.select(Account.createAdhoc(DatabaseKeys('account', {'expiry_date': 'account expiry_date TD', 'joined_date': 'account joined_date TD', 'plan_id': 98})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.name, 'account name TD')
        
        self.assertEqual(objs[0].vals.expiry_date, 'account expiry_date TD')
        self.assertEqual(objs[0].vals.joined_date, 'account joined_date TD')
        self.assertEqual(objs[0].vals.plan_id, 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestAccount.db.disableForeignKeys()

        TestAccount.db.upsert(
                Account('account name TD', 'account expiry_date TD UPD', 'account joined_date TD UPD', 100))
        objs = TestAccount.db.select(Account('account name TD'))
        self.assertEqual(len(objs), 1)

        d = eval("{'expiry_date': 'account expiry_date TD UPD', 'joined_date': 'account joined_date TD UPD', 'plan_id': 100}")
        for k, v in d.items():
            self.assertEqual(objs[0].vals.__getattribute__(k), v)

        TestAccount.db.rollback()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestAccount.db.disableForeignKeys()

        TestAccount.db.upsert(
                Account('account name TD INS', 'account expiry_date TD UPD', 'account joined_date TD UPD', 100))
        objs = TestAccount.db.select(Account())
        self.assertEqual(len(objs), 3)

        d = eval("{'expiry_date': 'account expiry_date TD UPD', 'joined_date': 'account joined_date TD UPD', 'plan_id': 100}")
        for k, v in d.items():
            self.assertEqual(objs[2].vals.__getattribute__(k), v)

        TestAccount.db.rollback()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestAccount.db.disableForeignKeys()

        TestAccount.db.delete(Account('account name TD'))

        objs = TestAccount.db.select(Account())
        self.assertEqual(len(objs), 1)

        TestAccount.db.rollback()

if __name__ == '__main__':
    import unittest
    unittest.main()
