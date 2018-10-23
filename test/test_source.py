# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.source import Source, SourceKeys, SourceValues
from Footy.src.database.database import Database, AdhocKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestSource(TestCase):
    """Source object tests"""
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
        keys =SourceKeys(98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Source.createAdhoc(AdhocKeys(None))
        self.assertEqual(l.getTable(), 'source')
        self.assertTrue(l._keys.getFields() is None)

    def test_createSingle(self):
        obj = Source.createSingle((98, 'source name TD', 'source fixtures_url TD', 'source url TD'))

        self.assertEqual(obj.getId(), 98)
         
        self.assertEqual(obj.getName(), 'source name TD')
        self.assertEqual(obj.getFixtures_Url(), 'source fixtures_url TD')
        self.assertEqual(obj.getUrl(), 'source url TD')
         

    def test_createMulti(self):
        rows = [(98, 'source name TD', 'source fixtures_url TD', 'source url TD'),
                (99, 'source name TD2', 'source fixtures_url TD2', 'source url TD2')]
        objs = Source.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'source name TD')
        self.assertEqual(objs[0].getFixtures_Url(), 'source fixtures_url TD')
        self.assertEqual(objs[0].getUrl(), 'source url TD')
        
        self.assertEqual(objs[1].getId(), 99)
        
        self.assertEqual(objs[1].getName(), 'source name TD2')
        self.assertEqual(objs[1].getFixtures_Url(), 'source fixtures_url TD2')
        self.assertEqual(objs[1].getUrl(), 'source url TD2')
        

    def test_repr(self):
        obj = Source(98, 'source name TD', 'source fixtures_url TD', 'source url TD')
        self.assertEqual(str(obj), "source : Keys {'id': 98} : Values {'name': 'source name TD', 'fixtures_url': 'source fixtures_url TD', 'url': 'source url TD'}")

    def test_select(self):
        objs = TestSource.db.select(Source())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'source name TD')
        self.assertEqual(objs[0].getFixtures_Url(), 'source fixtures_url TD')
        self.assertEqual(objs[0].getUrl(), 'source url TD')
        
        self.assertEqual(objs[1].getId(), 99)
        
        self.assertEqual(objs[1].getName(), 'source name TD2')
        self.assertEqual(objs[1].getFixtures_Url(), 'source fixtures_url TD2')
        self.assertEqual(objs[1].getUrl(), 'source url TD2')
        
        
        objs = TestSource.db.select(Source(98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'source name TD')
        self.assertEqual(objs[0].getFixtures_Url(), 'source fixtures_url TD')
        self.assertEqual(objs[0].getUrl(), 'source url TD')
        

        objs = TestSource.db.select(Source.createAdhoc(AdhocKeys({'name': 'source name TD', 'fixtures_url': 'source fixtures_url TD', 'url': 'source url TD'})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getId(), 98)
        
        self.assertEqual(objs[0].getName(), 'source name TD')
        self.assertEqual(objs[0].getFixtures_Url(), 'source fixtures_url TD')
        self.assertEqual(objs[0].getUrl(), 'source url TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestSource.db.disableForeignKeys()

        with TestSource.db.transaction() as t:
            TestSource.db.upsert(
                    Source(98, 'source name TD UPD', 'source fixtures_url TD UPD', 'source url TD UPD'))
            objs = TestSource.db.select(Source(98))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            d = eval("{'name': 'source name TD UPD', 'fixtures_url': 'source fixtures_url TD UPD', 'url': 'source url TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestSource.db.transaction() as t:
            source = TestSource.db.select(Source(98))[0]
            for k, v in d.items():
                source.__getattribute__('set' + k.title())(v)

            TestSource.db.upsert(source)

            objs = TestSource.db.select(Source(98))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getId(), 98)
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestSource.db.disableForeignKeys()

        with TestSource.db.transaction() as t:
            TestSource.db.upsert(
                    Source(100, 'source name TD UPD', 'source fixtures_url TD UPD', 'source url TD UPD'))
            objs = TestSource.db.select(Source())

            self.assertEqual(len(objs), 3)

            d = eval("{'id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'name': 'source name TD UPD', 'fixtures_url': 'source fixtures_url TD UPD', 'url': 'source url TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestSource.db.disableForeignKeys()

        with TestSource.db.transaction() as t:
            TestSource.db.delete(Source(98))

            objs = TestSource.db.select(Source())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Source()
        self.assertTrue(True and obj.isNullable('url')) 

if __name__ == '__main__':
    import unittest
    unittest.main()
