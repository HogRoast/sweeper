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
        keys =RatingKeys(98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.match_oid = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Rating.createAdhoc(None)
        self.assertEqual(l.getTable(), 'rating')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Rating.create((98, 98, 98))

        self.assertEqual(obj.getMatch_Oid(), 98)
         
        self.assertEqual(obj.getAlgo_Id(), 98)
        self.assertEqual(obj.getRank(), 98)
         

    def test_repr(self):
        obj = Rating(98, 98, 98)
        self.assertEqual(str(obj), "rating : Keys {'match_oid': 98} : Values {'algo_id': 98, 'rank': 98}")

    def test_select(self):
        objs = TestRating.db.select(Rating())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getMatch_Oid(), 98)
        
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        self.assertEqual(objs[0].getRank(), 98)
        
        self.assertEqual(objs[1].getMatch_Oid(), 99)
        
        self.assertEqual(objs[1].getAlgo_Id(), 99)
        self.assertEqual(objs[1].getRank(), 99)
        
        
        objs = TestRating.db.select(Rating(98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getMatch_Oid(), 98)
        
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        self.assertEqual(objs[0].getRank(), 98)
        

        objs = TestRating.db.select(Rating.createAdhoc({'algo_id': 98, 'rank': 98}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getMatch_Oid(), 98)
        
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        self.assertEqual(objs[0].getRank(), 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestRating.db.disableForeignKeys()

        with TestRating.db.transaction() as t:
            TestRating.db.upsert(
                    Rating(98, 100, 100))
            objs = TestRating.db.select(Rating(98))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getMatch_Oid(), 98)
            

            d = eval("{'algo_id': 100, 'rank': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestRating.db.transaction() as t:
            rating = TestRating.db.select(Rating(98))[0]
            for k, v in d.items():
                rating.__getattribute__('set' + k.title())(v)

            TestRating.db.upsert(rating)

            objs = TestRating.db.select(Rating(98))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getMatch_Oid(), 98)
            

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

            d = eval("{'match_oid': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'algo_id': 100, 'rank': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestRating.db.disableForeignKeys()

        with TestRating.db.transaction() as t:
            TestRating.db.delete(Rating(98))

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
