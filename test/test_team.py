# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.team import Team, TeamKeys, TeamValues
from Footy.src.database.database import Database, DatabaseKeys
from Footy.src.database.sqlite3_db import SQLite3Impl

class TestTeam(TestCase):
    """Team object tests"""
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
        keys =TeamKeys('team name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.name = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Team.createAdhoc(DatabaseKeys('team', None))
        self.assertEqual(l.keys.table, 'team')
        self.assertTrue(l.keys.fields is None)

    def test_createSingle(self):
        obj = Team.createSingle(('team name TD', 'league name TD'))

        self.assertEqual(obj.keys.name, 'team name TD')
         
        self.assertEqual(obj.vals.league, 'league name TD')
         

    def test_createMulti(self):
        rows = [('team name TD', 'league name TD'),
                ('team name TD2', 'league name TD2')]
        objs = Team.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.name, 'team name TD')
        
        self.assertEqual(objs[0].vals.league, 'league name TD')
        
        self.assertEqual(objs[1].keys.name, 'team name TD2')
        
        self.assertEqual(objs[1].vals.league, 'league name TD2')
        

    def test_repr(self):
        obj = Team('team name TD', 'league name TD')
        self.assertEqual(str(obj), "team : Keys {'name': 'team name TD'} : Values {'league': 'league name TD'}")

    def test_select(self):
        objs = TestTeam.db.select(Team())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.name, 'team name TD')
        
        self.assertEqual(objs[0].vals.league, 'league name TD')
        
        self.assertEqual(objs[1].keys.name, 'team name TD2')
        
        self.assertEqual(objs[1].vals.league, 'league name TD2')
        
        
        objs = TestTeam.db.select(Team('team name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.name, 'team name TD')
        
        self.assertEqual(objs[0].vals.league, 'league name TD')
        

        objs = TestTeam.db.select(Team.createAdhoc(DatabaseKeys('team', {'league': 'league name TD'})))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].keys.name, 'team name TD')
        
        self.assertEqual(objs[0].vals.league, 'league name TD')
        

if __name__ == '__main__':
    import unittest
    unittest.main()
