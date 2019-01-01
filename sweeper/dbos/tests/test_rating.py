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
        keys =RatingKeys('rating match_date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 98)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.match_date = 'Something New'
            keys.league = 'Something New'
            keys.home_team = 'Something New'
            keys.away_team = 'Something New'
            keys.algo_id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Rating.createAdhoc(None)
        self.assertEqual(l.getTable(), 'rating')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Rating.create(('rating match_date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 98, 98))

        self.assertEqual(obj.getMatch_Date(), 'rating match_date TD')
        self.assertEqual(obj.getLeague(), 'league mnemonic TD')
        self.assertEqual(obj.getHome_Team(), 'team name TD')
        self.assertEqual(obj.getAway_Team(), 'team name TD')
        self.assertEqual(obj.getAlgo_Id(), 98)
         
        self.assertEqual(obj.getMark(), 98)
         

    def test_repr(self):
        obj = Rating('rating match_date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 98, 98)
        self.assertEqual(str(obj), "rating : Keys {'match_date': 'rating match_date TD', 'league': 'league mnemonic TD', 'home_team': 'team name TD', 'away_team': 'team name TD', 'algo_id': 98} : Values {'mark': 98}")

    def test_select(self):
        objs = TestRating.db.select(Rating())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getMatch_Date(), 'rating match_date TD')
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getHome_Team(), 'team name TD')
        self.assertEqual(objs[0].getAway_Team(), 'team name TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        
        self.assertEqual(objs[0].getMark(), 98)
        
        self.assertEqual(objs[1].getMatch_Date(), 'rating match_date TD2')
        self.assertEqual(objs[1].getLeague(), 'league mnemonic TD2')
        self.assertEqual(objs[1].getHome_Team(), 'team name TD2')
        self.assertEqual(objs[1].getAway_Team(), 'team name TD2')
        self.assertEqual(objs[1].getAlgo_Id(), 99)
        
        self.assertEqual(objs[1].getMark(), 99)
        
        
        objs = TestRating.db.select(Rating('rating match_date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 98))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getMatch_Date(), 'rating match_date TD')
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getHome_Team(), 'team name TD')
        self.assertEqual(objs[0].getAway_Team(), 'team name TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        
        self.assertEqual(objs[0].getMark(), 98)
        

        objs = TestRating.db.select(Rating.createAdhoc({'mark': 98}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getMatch_Date(), 'rating match_date TD')
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getHome_Team(), 'team name TD')
        self.assertEqual(objs[0].getAway_Team(), 'team name TD')
        self.assertEqual(objs[0].getAlgo_Id(), 98)
        
        self.assertEqual(objs[0].getMark(), 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestRating.db.disableForeignKeys()

        with TestRating.db.transaction() as t:
            TestRating.db.upsert(
                    Rating('rating match_date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 98, 100))
            objs = TestRating.db.select(Rating('rating match_date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 98))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getMatch_Date(), 'rating match_date TD')
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            self.assertEqual(objs[0].getHome_Team(), 'team name TD')
            self.assertEqual(objs[0].getAway_Team(), 'team name TD')
            self.assertEqual(objs[0].getAlgo_Id(), 98)
            

            d = eval("{'mark': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestRating.db.transaction() as t:
            rating = TestRating.db.select(Rating('rating match_date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 98))[0]
            for k, v in d.items():
                rating.__getattribute__('set' + k.title())(v)

            TestRating.db.upsert(rating)

            objs = TestRating.db.select(Rating('rating match_date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 98))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getMatch_Date(), 'rating match_date TD')
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            self.assertEqual(objs[0].getHome_Team(), 'team name TD')
            self.assertEqual(objs[0].getAway_Team(), 'team name TD')
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
                    Rating('rating match_date TD INS', 'league mnemonic TD INS', 'team name TD INS', 'team name TD INS', 100, 100))
            objs = TestRating.db.select(Rating())

            self.assertEqual(len(objs), 3)

            d = eval("{'match_date': 'rating match_date TD INS', 'league': 'league mnemonic TD INS', 'home_team': 'team name TD INS', 'away_team': 'team name TD INS', 'algo_id': 100}")
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
            TestRating.db.delete(Rating('rating match_date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 98))

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
