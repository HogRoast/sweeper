# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.match import Match, MatchKeys, MatchValues
from Footy.src.database.database import Database, DatabaseKeys, AdhocKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestMatch(TestCase):
    """Match object tests"""
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
        keys =MatchKeys('match date TD', 'league name TD', 'team name TD', 'team name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.date = 'Something New'
            keys.league = 'Something New'
            keys.home_team = 'Something New'
            keys.away_team = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Match.createAdhoc(AdhocKeys('match', None))
        self.assertEqual(l.keys.table, 'match')
        self.assertTrue(l.keys.getFields() is None)

    def test_createSingle(self):
        obj = Match.createSingle(('match date TD', 'league name TD', 'team name TD', 'team name TD', 'X', 2.3))

        self.assertEqual(obj.keys.date, 'match date TD')
        self.assertEqual(obj.keys.league, 'league name TD')
        self.assertEqual(obj.keys.home_team, 'team name TD')
        self.assertEqual(obj.keys.away_team, 'team name TD')
         
        self.assertEqual(obj.vals.result, 'X')
        self.assertEqual(obj.vals.best_odds, 2.3)
         

    def test_createMulti(self):
        rows = [('match date TD', 'league name TD', 'team name TD', 'team name TD', 'X', 2.3),
                ('match date TD2', 'league name TD2', 'team name TD2', 'team name TD2', 'Z', 2.4)]
        objs = Match.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.date, 'match date TD')
        self.assertEqual(objs[0].keys.league, 'league name TD')
        self.assertEqual(objs[0].keys.home_team, 'team name TD')
        self.assertEqual(objs[0].keys.away_team, 'team name TD')
        
        self.assertEqual(objs[0].vals.result, 'X')
        self.assertEqual(objs[0].vals.best_odds, 2.3)
        
        self.assertEqual(objs[1].keys.date, 'match date TD2')
        self.assertEqual(objs[1].keys.league, 'league name TD2')
        self.assertEqual(objs[1].keys.home_team, 'team name TD2')
        self.assertEqual(objs[1].keys.away_team, 'team name TD2')
        
        self.assertEqual(objs[1].vals.result, 'Z')
        self.assertEqual(objs[1].vals.best_odds, 2.4)
        

    def test_repr(self):
        obj = Match('match date TD', 'league name TD', 'team name TD', 'team name TD', 'X', 2.3)
        self.assertEqual(str(obj), "match : Keys {'date': 'match date TD', 'league': 'league name TD', 'home_team': 'team name TD', 'away_team': 'team name TD'} : Values {'result': 'X', 'best_odds': 2.3}")

    def test_select(self):
        objs = TestMatch.db.select(Match())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.date, 'match date TD')
        self.assertEqual(objs[0].keys.league, 'league name TD')
        self.assertEqual(objs[0].keys.home_team, 'team name TD')
        self.assertEqual(objs[0].keys.away_team, 'team name TD')
        
        self.assertEqual(objs[0].vals.result, 'X')
        self.assertEqual(objs[0].vals.best_odds, 2.3)
        
        self.assertEqual(objs[1].keys.date, 'match date TD2')
        self.assertEqual(objs[1].keys.league, 'league name TD2')
        self.assertEqual(objs[1].keys.home_team, 'team name TD2')
        self.assertEqual(objs[1].keys.away_team, 'team name TD2')
        
        self.assertEqual(objs[1].vals.result, 'Z')
        self.assertEqual(objs[1].vals.best_odds, 2.4)
        
        
        objs = TestMatch.db.select(Match('match date TD', 'league name TD', 'team name TD', 'team name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.date, 'match date TD')
        self.assertEqual(objs[0].keys.league, 'league name TD')
        self.assertEqual(objs[0].keys.home_team, 'team name TD')
        self.assertEqual(objs[0].keys.away_team, 'team name TD')
        
        self.assertEqual(objs[0].vals.result, 'X')
        self.assertEqual(objs[0].vals.best_odds, 2.3)
        

        objs = TestMatch.db.select(Match.createAdhoc(AdhocKeys('match', {'result': 'X', 'best_odds': 2.3})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.date, 'match date TD')
        self.assertEqual(objs[0].keys.league, 'league name TD')
        self.assertEqual(objs[0].keys.home_team, 'team name TD')
        self.assertEqual(objs[0].keys.away_team, 'team name TD')
        
        self.assertEqual(objs[0].vals.result, 'X')
        self.assertEqual(objs[0].vals.best_odds, 2.3)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestMatch.db.disableForeignKeys()

        with TestMatch.db.transaction() as t:
            TestMatch.db.upsert(
                    Match('match date TD', 'league name TD', 'team name TD', 'team name TD', 'A', 5.6))
            objs = TestMatch.db.select(Match('match date TD', 'league name TD', 'team name TD', 'team name TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].keys.date, 'match date TD')
            self.assertEqual(objs[0].keys.league, 'league name TD')
            self.assertEqual(objs[0].keys.home_team, 'team name TD')
            self.assertEqual(objs[0].keys.away_team, 'team name TD')
            

            d = eval("{'result': 'A', 'best_odds': 5.6}")
            for k, v in d.items():
                self.assertEqual(objs[0].vals.__getattribute__(k), v)

            # force a rollback
            t.fail()

        with TestMatch.db.transaction() as t:
            match = TestMatch.db.select(Match('match date TD', 'league name TD', 'team name TD', 'team name TD'))[0]
            for k, v in d.items():
                object.__setattr__(match.vals, k, v)

            TestMatch.db.upsert(match)

            objs = TestMatch.db.select(Match('match date TD', 'league name TD', 'team name TD', 'team name TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].keys.date, 'match date TD')
            self.assertEqual(objs[0].keys.league, 'league name TD')
            self.assertEqual(objs[0].keys.home_team, 'team name TD')
            self.assertEqual(objs[0].keys.away_team, 'team name TD')
            

            for k, v in d.items():
                self.assertEqual(objs[0].vals.__getattribute__(k), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestMatch.db.disableForeignKeys()

        with TestMatch.db.transaction() as t:
            TestMatch.db.upsert(
                    Match('match date TD INS', 'league name TD INS', 'team name TD INS', 'team name TD INS', 'A', 5.6))
            objs = TestMatch.db.select(Match())

            self.assertEqual(len(objs), 3)

            d = eval("{'date': 'match date TD INS', 'league': 'league name TD INS', 'home_team': 'team name TD INS', 'away_team': 'team name TD INS'}")
            for k, v in d.items():
                self.assertEqual(objs[2].keys.__getattribute__(k), v)

            d = eval("{'result': 'A', 'best_odds': 5.6}")
            for k, v in d.items():
                self.assertEqual(objs[2].vals.__getattribute__(k), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestMatch.db.disableForeignKeys()

        with TestMatch.db.transaction() as t:
            TestMatch.db.delete(Match('match date TD', 'league name TD', 'team name TD', 'team name TD'))

            objs = TestMatch.db.select(Match())
            self.assertEqual(len(objs), 1)
            # force a rollback
            t.fail()

if __name__ == '__main__':
    import unittest
    unittest.main()
