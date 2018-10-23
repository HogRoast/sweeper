# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.match import Match, MatchKeys, MatchValues
from Footy.src.database.database import Database, AdhocKeys
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
        keys =MatchKeys('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.date = 'Something New'
            keys.league = 'Something New'
            keys.home_team = 'Something New'
            keys.away_team = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Match.createAdhoc(AdhocKeys(None))
        self.assertEqual(l.getTable(), 'match')
        self.assertTrue(l._keys.getFields() is None)

    def test_createSingle(self):
        obj = Match.createSingle(('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 'X', 2.3, 98, 98, 98, 98))

        self.assertEqual(obj.getDate(), 'match date TD')
        self.assertEqual(obj.getLeague(), 'league mnemonic TD')
        self.assertEqual(obj.getHome_Team(), 'team name TD')
        self.assertEqual(obj.getAway_Team(), 'team name TD')
         
        self.assertEqual(obj.getResult(), 'X')
        self.assertEqual(obj.getBest_Odds(), 2.3)
        self.assertEqual(obj.getHome_Goals(), 98)
        self.assertEqual(obj.getAway_Goals(), 98)
        self.assertEqual(obj.getHome_Lp(), 98)
        self.assertEqual(obj.getAway_Lp(), 98)
         

    def test_createMulti(self):
        rows = [('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 'X', 2.3, 98, 98, 98, 98),
                ('match date TD2', 'league mnemonic TD2', 'team name TD2', 'team name TD2', 'Z', 2.4, 99, 99, 99, 99)]
        objs = Match.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getDate(), 'match date TD')
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getHome_Team(), 'team name TD')
        self.assertEqual(objs[0].getAway_Team(), 'team name TD')
        
        self.assertEqual(objs[0].getResult(), 'X')
        self.assertEqual(objs[0].getBest_Odds(), 2.3)
        self.assertEqual(objs[0].getHome_Goals(), 98)
        self.assertEqual(objs[0].getAway_Goals(), 98)
        self.assertEqual(objs[0].getHome_Lp(), 98)
        self.assertEqual(objs[0].getAway_Lp(), 98)
        
        self.assertEqual(objs[1].getDate(), 'match date TD2')
        self.assertEqual(objs[1].getLeague(), 'league mnemonic TD2')
        self.assertEqual(objs[1].getHome_Team(), 'team name TD2')
        self.assertEqual(objs[1].getAway_Team(), 'team name TD2')
        
        self.assertEqual(objs[1].getResult(), 'Z')
        self.assertEqual(objs[1].getBest_Odds(), 2.4)
        self.assertEqual(objs[1].getHome_Goals(), 99)
        self.assertEqual(objs[1].getAway_Goals(), 99)
        self.assertEqual(objs[1].getHome_Lp(), 99)
        self.assertEqual(objs[1].getAway_Lp(), 99)
        

    def test_repr(self):
        obj = Match('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 'X', 2.3, 98, 98, 98, 98)
        self.assertEqual(str(obj), "match : Keys {'date': 'match date TD', 'league': 'league mnemonic TD', 'home_team': 'team name TD', 'away_team': 'team name TD'} : Values {'result': 'X', 'best_odds': 2.3, 'home_goals': 98, 'away_goals': 98, 'home_lp': 98, 'away_lp': 98}")

    def test_select(self):
        objs = TestMatch.db.select(Match())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getDate(), 'match date TD')
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getHome_Team(), 'team name TD')
        self.assertEqual(objs[0].getAway_Team(), 'team name TD')
        
        self.assertEqual(objs[0].getResult(), 'X')
        self.assertEqual(objs[0].getBest_Odds(), 2.3)
        self.assertEqual(objs[0].getHome_Goals(), 98)
        self.assertEqual(objs[0].getAway_Goals(), 98)
        self.assertEqual(objs[0].getHome_Lp(), 98)
        self.assertEqual(objs[0].getAway_Lp(), 98)
        
        self.assertEqual(objs[1].getDate(), 'match date TD2')
        self.assertEqual(objs[1].getLeague(), 'league mnemonic TD2')
        self.assertEqual(objs[1].getHome_Team(), 'team name TD2')
        self.assertEqual(objs[1].getAway_Team(), 'team name TD2')
        
        self.assertEqual(objs[1].getResult(), 'Z')
        self.assertEqual(objs[1].getBest_Odds(), 2.4)
        self.assertEqual(objs[1].getHome_Goals(), 99)
        self.assertEqual(objs[1].getAway_Goals(), 99)
        self.assertEqual(objs[1].getHome_Lp(), 99)
        self.assertEqual(objs[1].getAway_Lp(), 99)
        
        
        objs = TestMatch.db.select(Match('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getDate(), 'match date TD')
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getHome_Team(), 'team name TD')
        self.assertEqual(objs[0].getAway_Team(), 'team name TD')
        
        self.assertEqual(objs[0].getResult(), 'X')
        self.assertEqual(objs[0].getBest_Odds(), 2.3)
        self.assertEqual(objs[0].getHome_Goals(), 98)
        self.assertEqual(objs[0].getAway_Goals(), 98)
        self.assertEqual(objs[0].getHome_Lp(), 98)
        self.assertEqual(objs[0].getAway_Lp(), 98)
        

        objs = TestMatch.db.select(Match.createAdhoc(AdhocKeys({'result': 'X', 'best_odds': 2.3, 'home_goals': 98, 'away_goals': 98, 'home_lp': 98, 'away_lp': 98})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getDate(), 'match date TD')
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getHome_Team(), 'team name TD')
        self.assertEqual(objs[0].getAway_Team(), 'team name TD')
        
        self.assertEqual(objs[0].getResult(), 'X')
        self.assertEqual(objs[0].getBest_Odds(), 2.3)
        self.assertEqual(objs[0].getHome_Goals(), 98)
        self.assertEqual(objs[0].getAway_Goals(), 98)
        self.assertEqual(objs[0].getHome_Lp(), 98)
        self.assertEqual(objs[0].getAway_Lp(), 98)
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestMatch.db.disableForeignKeys()

        with TestMatch.db.transaction() as t:
            TestMatch.db.upsert(
                    Match('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD', 'A', 5.6, 100, 100, 100, 100))
            objs = TestMatch.db.select(Match('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getDate(), 'match date TD')
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            self.assertEqual(objs[0].getHome_Team(), 'team name TD')
            self.assertEqual(objs[0].getAway_Team(), 'team name TD')
            

            d = eval("{'result': 'A', 'best_odds': 5.6, 'home_goals': 100, 'away_goals': 100, 'home_lp': 100, 'away_lp': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestMatch.db.transaction() as t:
            match = TestMatch.db.select(Match('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD'))[0]
            for k, v in d.items():
                match.__getattribute__('set' + k.title())(v)

            TestMatch.db.upsert(match)

            objs = TestMatch.db.select(Match('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getDate(), 'match date TD')
            self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
            self.assertEqual(objs[0].getHome_Team(), 'team name TD')
            self.assertEqual(objs[0].getAway_Team(), 'team name TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestMatch.db.disableForeignKeys()

        with TestMatch.db.transaction() as t:
            TestMatch.db.upsert(
                    Match('match date TD INS', 'league mnemonic TD INS', 'team name TD INS', 'team name TD INS', 'A', 5.6, 100, 100, 100, 100))
            objs = TestMatch.db.select(Match())

            self.assertEqual(len(objs), 3)

            d = eval("{'date': 'match date TD INS', 'league': 'league mnemonic TD INS', 'home_team': 'team name TD INS', 'away_team': 'team name TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'result': 'A', 'best_odds': 5.6, 'home_goals': 100, 'away_goals': 100, 'home_lp': 100, 'away_lp': 100}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestMatch.db.disableForeignKeys()

        with TestMatch.db.transaction() as t:
            TestMatch.db.delete(Match('match date TD', 'league mnemonic TD', 'team name TD', 'team name TD'))

            objs = TestMatch.db.select(Match())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Match()
        self.assertTrue(True and obj.isNullable('result') and obj.isNullable('best_odds') and obj.isNullable('home_goals') and obj.isNullable('away_goals') and obj.isNullable('home_lp') and obj.isNullable('away_lp')) 

if __name__ == '__main__':
    import unittest
    unittest.main()
