# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from sweeper.dbos.algo_config import Algo_Config, Algo_ConfigKeys, Algo_ConfigValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestAlgo_Config(TestCase):
    """Algo_Config object tests"""
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
        keys =Algo_ConfigKeys('algo_config config_date TD', 98, 'league mnemonic TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.config_date = 'Something New'
            keys.algo_id = 75
            keys.league = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Algo_Config.createAdhoc(None)
        self.assertEqual(l.getTable(), 'algo_config')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Algo_Config.create(('algo_config config_date TD', 98, 'league mnemonic TD', 98, 98))

        self.assertEqual(obj.getConfig_Date(), 'algo_config config_date TD')
        self.assertEqual(obj.getAlgo_Id(), 98)
        self.assertEqual(obj.getLeague(), 'league mnemonic TD')
         
        self.assertEqual(obj.getL_Bnd_Mark(), 98)
        self.assertEqual(obj.getU_Bnd_Mark(), 98)
         

    def test_repr(self):
        obj = Algo_Config('algo_config config_date TD', 98, 'league mnemonic TD', 98, 98)
        self.assertEqual(str(obj), "algo_config : Keys {'config_date': 'algo_config config_date TD', 'algo_id': 98, 'league': 'league mnemonic TD'} : Values {'l_bnd_mark': 98, 'u_bnd_mark': 98}")

    def test_select(self):
        objs = TestAlgo_Config.db.select(Algo_Config())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getConfig_Date(), 'algo_config config_date TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getL_Bnd_Mark(), 98)
        self.assertEqual(objs[0].getU_Bnd_Mark(), 98)
        
        self.assertEqual(objs[1].getConfig_Date(), 'algo_config config_date TD2')
        self.assertEqual(objs[1].getAlgo_Id(), 99)
        self.assertEqual(objs[1].getLeague(), 'league mnemonic TD2')
        
        self.assertEqual(objs[1].getL_Bnd_Mark(), 99)
        self.assertEqual(objs[1].getU_Bnd_Mark(), 99)
        
        
        objs = TestAlgo_Config.db.select(Algo_Config('algo_config config_date TD', 98, 'league mnemonic TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getConfig_Date(), 'algo_config config_date TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getL_Bnd_Mark(), 98)
        self.assertEqual(objs[0].getU_Bnd_Mark(), 98)
        

        objs = TestAlgo_Config.db.select(Algo_Config.createAdhoc({'l_bnd_mark': 98, 'u_bnd_mark': 98}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getConfig_Date(), 'algo_config config_date TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        
        self.assertEqual(objs[0].getL_Bnd_Mark(), 98)
        self.assertEqual(objs[0].getU_Bnd_Mark(), 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestAlgo_Config.db.disableForeignKeys()

        with TestAlgo_Config.db.transaction() as t:
            TestAlgo_Config.db.upsert(
                    Algo_Config('algo_config config_date TD', 98, 'league mnemonic TD', 100, 100))
            objs = TestAlgo_Config.db.select(Algo_Config('algo_config config_date TD', 98, 'league mnemonic TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getConfig_Date(), 'algo_config config_date TD')
            self.assertEqual(objs[0].getAlgo_Id(), 98)
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            

            d = eval("{'l_bnd_mark': 100, 'u_bnd_mark': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestAlgo_Config.db.transaction() as t:
            algo_config = TestAlgo_Config.db.select(Algo_Config('algo_config config_date TD', 98, 'league mnemonic TD'))[0]
            for k, v in d.items():
                algo_config.__getattribute__('set' + k.title())(v)

            TestAlgo_Config.db.upsert(algo_config)

            objs = TestAlgo_Config.db.select(Algo_Config('algo_config config_date TD', 98, 'league mnemonic TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getConfig_Date(), 'algo_config config_date TD')
            self.assertEqual(objs[0].getAlgo_Id(), 98)
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestAlgo_Config.db.disableForeignKeys()

        with TestAlgo_Config.db.transaction() as t:
            TestAlgo_Config.db.upsert(
                    Algo_Config('algo_config config_date TD INS', 100, 'league mnemonic TD INS', 100, 100))
            objs = TestAlgo_Config.db.select(Algo_Config())

            self.assertEqual(len(objs), 3)

            d = eval("{'config_date': 'algo_config config_date TD INS', 'algo_id': 100, 'league': 'league mnemonic TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'l_bnd_mark': 100, 'u_bnd_mark': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestAlgo_Config.db.disableForeignKeys()

        with TestAlgo_Config.db.transaction() as t:
            TestAlgo_Config.db.delete(Algo_Config('algo_config config_date TD', 98, 'league mnemonic TD'))

            objs = TestAlgo_Config.db.select(Algo_Config())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Algo_Config()
        self.assertTrue(True) 

if __name__ == '__main__':
    import unittest
    unittest.main()
