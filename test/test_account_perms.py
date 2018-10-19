# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.account_perms import Account_Perms, Account_PermsKeys, Account_PermsValues
from Footy.src.database.database import Database, AdhocKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestAccount_Perms(TestCase):
    """Account_Perms object tests"""
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
        keys =Account_PermsKeys(98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Account_Perms.createAdhoc(AdhocKeys(None))
        self.assertEqual(l.getTable(), 'account_perms')
        self.assertTrue(l._keys.getFields() is None)

    def test_createSingle(self):
        obj = Account_Perms.createSingle((98, 'account name TD', 'league name TD', 98))

        self.assertEqual(obj.getId(), 98)
         
        self.assertEqual(obj.getAccount(), 'account name TD')
        self.assertEqual(obj.getLeague(), 'league name TD')
        self.assertEqual(obj.getAlgo_Id(), 98)
         

    def test_createMulti(self):
        rows = [(98, 'account name TD', 'league name TD', 98),
                (99, 'account name TD2', 'league name TD2', 99)]
        objs = Account_Perms.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getAccount(), 'account name TD')
        self.assertEqual(objs[0].getLeague(), 'league name TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        
        self.assertEqual(objs[1].getId(), 99)
        
        self.assertEqual(objs[1].getAccount(), 'account name TD2')
        self.assertEqual(objs[1].getLeague(), 'league name TD2')
        self.assertEqual(objs[1].getAlgo_Id(), 99)
        

    def test_repr(self):
        obj = Account_Perms(98, 'account name TD', 'league name TD', 98)
        self.assertEqual(str(obj), "account_perms : Keys {'id': 98} : Values {'account': 'account name TD', 'league': 'league name TD', 'algo_id': 98}")

    def test_select(self):
        objs = TestAccount_Perms.db.select(Account_Perms())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getAccount(), 'account name TD')
        self.assertEqual(objs[0].getLeague(), 'league name TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        
        self.assertEqual(objs[1].getId(), 99)
        
        self.assertEqual(objs[1].getAccount(), 'account name TD2')
        self.assertEqual(objs[1].getLeague(), 'league name TD2')
        self.assertEqual(objs[1].getAlgo_Id(), 99)
        
        
        objs = TestAccount_Perms.db.select(Account_Perms(98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getAccount(), 'account name TD')
        self.assertEqual(objs[0].getLeague(), 'league name TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        

        objs = TestAccount_Perms.db.select(Account_Perms.createAdhoc(AdhocKeys({'account': 'account name TD', 'league': 'league name TD', 'algo_id': 98})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getAccount(), 'account name TD')
        self.assertEqual(objs[0].getLeague(), 'league name TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestAccount_Perms.db.disableForeignKeys()

        with TestAccount_Perms.db.transaction() as t:
            TestAccount_Perms.db.upsert(
                    Account_Perms(98, 'account name TD UPD', 'league name TD UPD', 100))
            objs = TestAccount_Perms.db.select(Account_Perms(98))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            d = eval("{'account': 'account name TD UPD', 'league': 'league name TD UPD', 'algo_id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestAccount_Perms.db.transaction() as t:
            account_perms = TestAccount_Perms.db.select(Account_Perms(98))[0]
            for k, v in d.items():
                account_perms.__getattribute__('set' + k.title())(v)

            TestAccount_Perms.db.upsert(account_perms)

            objs = TestAccount_Perms.db.select(Account_Perms(98))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestAccount_Perms.db.disableForeignKeys()

        with TestAccount_Perms.db.transaction() as t:
            TestAccount_Perms.db.upsert(
                    Account_Perms(100, 'account name TD UPD', 'league name TD UPD', 100))
            objs = TestAccount_Perms.db.select(Account_Perms())

            self.assertEqual(len(objs), 3)

            d = eval("{'id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'account': 'account name TD UPD', 'league': 'league name TD UPD', 'algo_id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestAccount_Perms.db.disableForeignKeys()

        with TestAccount_Perms.db.transaction() as t:
            TestAccount_Perms.db.delete(Account_Perms(98))

            objs = TestAccount_Perms.db.select(Account_Perms())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

if __name__ == '__main__':
    import unittest
    unittest.main()
