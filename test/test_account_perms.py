# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.account_perms import Account_perms, Account_permsKeys, Account_permsValues
from Footy.src.database.database import Database, DatabaseKeys, AdhocKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestAccount_perms(TestCase):
    """Account_perms object tests"""
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
        keys =Account_permsKeys(98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Account_perms.createAdhoc(AdhocKeys('account_perms', None))
        self.assertEqual(l.keys.table, 'account_perms')
        self.assertTrue(l.keys.getFields() is None)

    def test_createSingle(self):
        obj = Account_perms.createSingle((98, 'account name TD', 'league name TD', 98))

        self.assertEqual(obj.keys.id, 98)
         
        self.assertEqual(obj.vals.account, 'account name TD')
        self.assertEqual(obj.vals.league, 'league name TD')
        self.assertEqual(obj.vals.algo_id, 98)
         

    def test_createMulti(self):
        rows = [(98, 'account name TD', 'league name TD', 98),
                (99, 'account name TD2', 'league name TD2', 99)]
        objs = Account_perms.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.account, 'account name TD')
        self.assertEqual(objs[0].vals.league, 'league name TD')
        self.assertEqual(objs[0].vals.algo_id, 98)
        
        self.assertEqual(objs[1].keys.id, 99)
        
        self.assertEqual(objs[1].vals.account, 'account name TD2')
        self.assertEqual(objs[1].vals.league, 'league name TD2')
        self.assertEqual(objs[1].vals.algo_id, 99)
        

    def test_repr(self):
        obj = Account_perms(98, 'account name TD', 'league name TD', 98)
        self.assertEqual(str(obj), "account_perms : Keys {'id': 98} : Values {'account': 'account name TD', 'league': 'league name TD', 'algo_id': 98}")

    def test_select(self):
        objs = TestAccount_perms.db.select(Account_perms())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.account, 'account name TD')
        self.assertEqual(objs[0].vals.league, 'league name TD')
        self.assertEqual(objs[0].vals.algo_id, 98)
        
        self.assertEqual(objs[1].keys.id, 99)
        
        self.assertEqual(objs[1].vals.account, 'account name TD2')
        self.assertEqual(objs[1].vals.league, 'league name TD2')
        self.assertEqual(objs[1].vals.algo_id, 99)
        
        
        objs = TestAccount_perms.db.select(Account_perms(98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.account, 'account name TD')
        self.assertEqual(objs[0].vals.league, 'league name TD')
        self.assertEqual(objs[0].vals.algo_id, 98)
        

        objs = TestAccount_perms.db.select(Account_perms.createAdhoc(AdhocKeys('account_perms', {'account': 'account name TD', 'league': 'league name TD', 'algo_id': 98})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.id, 98)
        
        self.assertEqual(objs[0].vals.account, 'account name TD')
        self.assertEqual(objs[0].vals.league, 'league name TD')
        self.assertEqual(objs[0].vals.algo_id, 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestAccount_perms.db.disableForeignKeys()

        with TestAccount_perms.db.transaction() as t:
            TestAccount_perms.db.upsert(
                    Account_perms(98, 'account name TD UPD', 'league name TD UPD', 100))
            objs = TestAccount_perms.db.select(Account_perms(98))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].keys.id, 98)
            

            d = eval("{'account': 'account name TD UPD', 'league': 'league name TD UPD', 'algo_id': 100}")
            for k, v in d.items():
                self.assertEqual(objs[0].vals.__getattribute__(k), v)

            # force a rollback
            t.fail()

        with TestAccount_perms.db.transaction() as t:
            account_perms = TestAccount_perms.db.select(Account_perms(98))[0]
            for k, v in d.items():
                object.__setattr__(account_perms.vals, k, v)

            TestAccount_perms.db.upsert(account_perms)

            objs = TestAccount_perms.db.select(Account_perms(98))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].keys.id, 98)
            

            for k, v in d.items():
                self.assertEqual(objs[0].vals.__getattribute__(k), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestAccount_perms.db.disableForeignKeys()

        with TestAccount_perms.db.transaction() as t:
            TestAccount_perms.db.upsert(
                    Account_perms(100, 'account name TD UPD', 'league name TD UPD', 100))
            objs = TestAccount_perms.db.select(Account_perms())

            self.assertEqual(len(objs), 3)

            d = eval("{'id': 100}")
            for k, v in d.items():
                self.assertEqual(objs[2].keys.__getattribute__(k), v)

            d = eval("{'account': 'account name TD UPD', 'league': 'league name TD UPD', 'algo_id': 100}")
            for k, v in d.items():
                self.assertEqual(objs[2].vals.__getattribute__(k), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestAccount_perms.db.disableForeignKeys()

        with TestAccount_perms.db.transaction() as t:
            TestAccount_perms.db.delete(Account_perms(98))

            objs = TestAccount_perms.db.select(Account_perms())
            self.assertEqual(len(objs), 1)
            # force a rollback
            t.fail()

if __name__ == '__main__':
    import unittest
    unittest.main()
