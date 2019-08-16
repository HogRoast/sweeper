# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from sweeper.dbos.team import Team, TeamKeys, TeamValues
from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

class TestTeam(TestCase):
    """Team object tests"""
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
        keys =TeamKeys('team name TD')

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.name = 'Something New'
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Team.createAdhoc(None)
        self.assertEqual(l.getTable(), 'team')
        self.assertTrue(l._keys.getFields() is None)

    def test_create(self):
        obj = Team.create(('team name TD', 'league mnemonic TD', 'team season TD'))

        self.assertEqual(obj.getName(), 'team name TD')
         
        self.assertEqual(obj.getLeague(), 'league mnemonic TD')
        self.assertEqual(obj.getSeason(), 'team season TD')
         

    def test_repr(self):
        obj = Team('team name TD', 'league mnemonic TD', 'team season TD')
        self.assertEqual(str(obj), "team : Keys {'name': 'team name TD'} : Values {'league': 'league mnemonic TD', 'season': 'team season TD'}")

    def test_select(self):
        objs = TestTeam.db.select(Team())
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].getName(), 'team name TD')
        
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getSeason(), 'team season TD')
        
        self.assertEqual(objs[1].getName(), 'team name TD2')
        
        self.assertEqual(objs[1].getLeague(), 'league mnemonic TD2')
        self.assertEqual(objs[1].getSeason(), 'team season TD2')
        
        
        objs = TestTeam.db.select(Team('team name TD'))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getName(), 'team name TD')
        
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getSeason(), 'team season TD')
        

        objs = TestTeam.db.select(Team.createAdhoc({'league': 'league mnemonic TD', 'season': 'team season TD'}))
        self.assertEqual(len(objs), 1)
        self.assertEqual(objs[0].getName(), 'team name TD')
        
        self.assertEqual(objs[0].getLeague(), 'league mnemonic TD')
        self.assertEqual(objs[0].getSeason(), 'team season TD')
        

    def test_update(self):
        # Disable Foreign Keys checks for this test
        TestTeam.db.disableForeignKeys()

        with TestTeam.db.transaction() as t:
            TestTeam.db.upsert(
                    Team('team name TD', 'league mnemonic TD UPD', 'team season TD UPD'))
            objs = TestTeam.db.select(Team('team name TD'))

            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getName(), 'team name TD')
            

            d = eval("{'league': 'league mnemonic TD UPD', 'season': 'team season TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

        with TestTeam.db.transaction() as t:
            team = TestTeam.db.select(Team('team name TD'))[0]
            for k, v in d.items():
                team.__getattribute__('set' + k.title())(v)

            TestTeam.db.upsert(team)

            objs = TestTeam.db.select(Team('team name TD'))
            self.assertEqual(len(objs), 1)
            self.assertEqual(objs[0].getName(), 'team name TD')
            

            for k, v in d.items():
                self.assertEqual(
                        objs[0].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_insert(self):
        # Disable Foreign Keys checks for this test
        TestTeam.db.disableForeignKeys()

        with TestTeam.db.transaction() as t:
            TestTeam.db.upsert(
                    Team('team name TD INS', 'league mnemonic TD UPD', 'team season TD UPD'))
            objs = TestTeam.db.select(Team())

            self.assertEqual(len(objs), 3)

            d = eval("{'name': 'team name TD INS'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            d = eval("{'league': 'league mnemonic TD UPD', 'season': 'team season TD UPD'}")
            for k, v in d.items():
                self.assertEqual(
                        objs[2].__getattribute__('get' + k.title())(), v)

            # force a rollback
            t.fail()

    def test_delete(self):
        # Disable Foreign Keys checks for this test
        TestTeam.db.disableForeignKeys()

        with TestTeam.db.transaction() as t:
            TestTeam.db.delete(Team('team name TD'))

            objs = TestTeam.db.select(Team())
            self.assertEqual(len(objs), 1)

            # force a rollback
            t.fail()

    def test_isNullable(self):
        obj = Team()
        self.assertTrue(True) 

if __name__ == '__main__':
    import unittest
    unittest.main()
