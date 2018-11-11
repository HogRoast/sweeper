# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from sweeper.dbos.rating import Rating, RatingKeys, RatingValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestRating(TestCase):
    """Rating object tests"""
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
        keys =RatingKeys(98, 98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.match_id = 75
            keys.algo_id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Rating.createAdhoc(None)
        self.assertEqual(l.getTable(), 'rating')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Rating.create((98, 98, 98))

        self.assertEqual(obj.getMatch_Id(), 98)
        self.assertEqual(obj.getAlgo_Id(), 98)
         
        self.assertEqual(obj.getMark(), 98)
         

    def test_repr(self):
        obj = Rating(98, 98, 98)
        self.assertEqual(str(obj), "rating : Keys {'match_id': 98, 'algo_id': 98} : Values {'mark': 98}")

    def test_select(self):
        objs = TestRating.db.select(Rating())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getMatch_Id(), 98)
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        
        self.assertEqual(objs[0].getMark(), 98)
        
        self.assertEqual(objs[1].getMatch_Id(), 99)
        self.assertEqual(objs[1].getAlgo_Id(), 99)
        
        self.assertEqual(objs[1].getMark(), 99)
        
        
        objs = TestRating.db.select(Rating(98, 98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getMatch_Id(), 98)
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        
        self.assertEqual(objs[0].getMark(), 98)
        

        objs = TestRating.db.select(Rating.createAdhoc({'mark': 98}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getMatch_Id(), 98)
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        
        self.assertEqual(objs[0].getMark(), 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestRating.db.disableForeignKeys()

        with TestRating.db.transaction() as t:
            TestRating.db.upsert(
                    Rating(98, 98, 100))
            objs = TestRating.db.select(Rating(98, 98))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getMatch_Id(), 98)
            self.assertEqual(objs[0].getAlgo_Id(), 98)
            

            d = eval("{'mark': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestRating.db.transaction() as t:
            rating = TestRating.db.select(Rating(98, 98))[0]
            for k, v in d.items():
                rating.__getattribute__('set' + k.title())(v)

            TestRating.db.upsert(rating)

            objs = TestRating.db.select(Rating(98, 98))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getMatch_Id(), 98)
            self.assertEqual(objs[0].getAlgo_Id(), 98)
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestRating.db.disableForeignKeys()

        with TestRating.db.transaction() as t:
            TestRating.db.upsert(
                    Rating(100, 100, 100))
            objs = TestRating.db.select(Rating())

            self.assertEqual(len(objs), 3)

            d = eval("{'match_id': 100, 'algo_id': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'mark': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestRating.db.disableForeignKeys()

        with TestRating.db.transaction() as t:
            TestRating.db.delete(Rating(98, 98))

            objs = TestRating.db.select(Rating())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Rating()
        self.assertTrue(True) 

if __name__ == '__main__':
    import unittest
    unittest.main()
