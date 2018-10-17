# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.match import Match, MatchKeys, MatchValues
from Footy.src.database.database import Database, DatabaseKeys
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
        cls.db.enableForeignKeys()

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
        l = Match.createAdhoc(DatabaseKeys('match', None))
        self.assertEqual(l.keys.table, 'match')
        self.assertTrue(l.keys.fields is None)

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
        

        objs = TestMatch.db.select(Match.createAdhoc(DatabaseKeys('match', {'result': 'X', 'best_odds': 2.3})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.date, 'match date TD')
        self.assertEqual(objs[0].keys.league, 'league name TD')
        self.assertEqual(objs[0].keys.home_team, 'team name TD')
        self.assertEqual(objs[0].keys.away_team, 'team name TD')
        
        self.assertEqual(objs[0].vals.result, 'X')
        self.assertEqual(objs[0].vals.best_odds, 2.3)
        

if __name__ == '__main__':
    import unittest
    unittest.main()
