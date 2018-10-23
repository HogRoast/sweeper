# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.season import Season, SeasonKeys, SeasonValues
from Footy.src.database.database import Database, AdhocKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestSeason(TestCase):
    """Season object tests"""
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
        keys =SeasonKeys('season name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.name = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Season.createAdhoc(AdhocKeys(None))
        self.assertEqual(l.getTable(), 'season')
        self.assertTrue(l._keys.getFields() is None)

    def test_createSingle(self):
        obj = Season.createSingle(('season name TD', 'season l_bnd_date TD', 'season u_bnd_date TD'))

        self.assertEqual(obj.getName(), 'season name TD')
         
        self.assertEqual(obj.getL_Bnd_Date(), 'season l_bnd_date TD')
        self.assertEqual(obj.getU_Bnd_Date(), 'season u_bnd_date TD')
         

    def test_createMulti(self):
        rows = [('season name TD', 'season l_bnd_date TD', 'season u_bnd_date TD'),
                ('season name TD2', 'season l_bnd_date TD2', 'season u_bnd_date TD2')]
        objs = Season.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getName(), 'season name TD')
        
        self.assertEqual(objs[0].getL_Bnd_Date(), 'season l_bnd_date TD')
        self.assertEqual(objs[0].getU_Bnd_Date(), 'season u_bnd_date TD')
        
        self.assertEqual(objs[1].getName(), 'season name TD2')
        
        self.assertEqual(objs[1].getL_Bnd_Date(), 'season l_bnd_date TD2')
        self.assertEqual(objs[1].getU_Bnd_Date(), 'season u_bnd_date TD2')
        

    def test_repr(self):
        obj = Season('season name TD', 'season l_bnd_date TD', 'season u_bnd_date TD')
        self.assertEqual(str(obj), "season : Keys {'name': 'season name TD'} : Values {'l_bnd_date': 'season l_bnd_date TD', 'u_bnd_date': 'season u_bnd_date TD'}")

    def test_select(self):
        objs = TestSeason.db.select(Season())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getName(), 'season name TD')
        
        self.assertEqual(objs[0].getL_Bnd_Date(), 'season l_bnd_date TD')
        self.assertEqual(objs[0].getU_Bnd_Date(), 'season u_bnd_date TD')
        
        self.assertEqual(objs[1].getName(), 'season name TD2')
        
        self.assertEqual(objs[1].getL_Bnd_Date(), 'season l_bnd_date TD2')
        self.assertEqual(objs[1].getU_Bnd_Date(), 'season u_bnd_date TD2')
        
        
        objs = TestSeason.db.select(Season('season name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getName(), 'season name TD')
        
        self.assertEqual(objs[0].getL_Bnd_Date(), 'season l_bnd_date TD')
        self.assertEqual(objs[0].getU_Bnd_Date(), 'season u_bnd_date TD')
        

        objs = TestSeason.db.select(Season.createAdhoc(AdhocKeys({'l_bnd_date': 'season l_bnd_date TD', 'u_bnd_date': 'season u_bnd_date TD'})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getName(), 'season name TD')
        
        self.assertEqual(objs[0].getL_Bnd_Date(), 'season l_bnd_date TD')
        self.assertEqual(objs[0].getU_Bnd_Date(), 'season u_bnd_date TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestSeason.db.disableForeignKeys()

        with TestSeason.db.transaction() as t:
            TestSeason.db.upsert(
                    Season('season name TD', 'season l_bnd_date TD UPD', 'season u_bnd_date TD UPD'))
            objs = TestSeason.db.select(Season('season name TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getName(), 'season name TD')
            

            d = eval("{'l_bnd_date': 'season l_bnd_date TD UPD', 'u_bnd_date': 'season u_bnd_date TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestSeason.db.transaction() as t:
            season = TestSeason.db.select(Season('season name TD'))[0]
            for k, v in d.items():
                season.__getattribute__('set' + k.title())(v)

            TestSeason.db.upsert(season)

            objs = TestSeason.db.select(Season('season name TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getName(), 'season name TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestSeason.db.disableForeignKeys()

        with TestSeason.db.transaction() as t:
            TestSeason.db.upsert(
                    Season('season name TD INS', 'season l_bnd_date TD UPD', 'season u_bnd_date TD UPD'))
            objs = TestSeason.db.select(Season())

            self.assertEqual(len(objs), 3)

            d = eval("{'name': 'season name TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'l_bnd_date': 'season l_bnd_date TD UPD', 'u_bnd_date': 'season u_bnd_date TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestSeason.db.disableForeignKeys()

        with TestSeason.db.transaction() as t:
            TestSeason.db.delete(Season('season name TD'))

            objs = TestSeason.db.select(Season())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

if __name__ == '__main__':
    import unittest
    unittest.main()
