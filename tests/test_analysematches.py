# coding: utf-8

import configparser, sys, csv, os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call

from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl

from sweeper.dbos.statistics import Statistics
from sweeper.dbos.rating import Rating
from sweeper.dbos.match import Match
from analysematches import analyseMatches

class TestAnalyseMatches(TestCase):
    """AnalyseMatches tests"""

    def mock_getSweeperConfig(self):
        baseCfg = {'dbName' : './db/test.db'}
        return baseCfg

    def mockGlobals(self):
        self.orig_getSweeperConfig = analyseMatches.__globals__['getSweeperConfig']
        self.orig_Logger = analyseMatches.__globals__['Logger']

        analyseMatches.__globals__['getSweeperConfig'] = self.mock_getSweeperConfig
        analyseMatches.__globals__['Logger'] = self.mock_Logger

    def resetGlobals(self):
        analyseMatches.__globals__['getSweeperConfig'] = self.orig_getSweeperConfig
        analyseMatches.__globals__['Logger'] = self.orig_Logger

    def initialiseData(self):
        with Database(self.dbName, SQLite3Impl()) as db, db.transaction() as t:
            db.upsert(Match(201809011, '2018-09-01', 'league mnemonic TD', \
                    'team name TD', 'team name TD2', 'H', 2.6, 3.1, 3.2, 2, 1))
            db.upsert(Match(201809021, '2018-09-02', 'league mnemonic TD', \
                    'team name TD', 'team name TD2', 'D', 2.6, 3.1, 3.2, 1, 1))
            db.upsert(Match(201809031, '2018-09-03', 'league mnemonic TD', \
                    'team name TD', 'team name TD2', 'A', 2.6, 3.1, 3.2, 0, 3))
            db.upsert(Match(201809041, '2018-09-04', 'league mnemonic TD', \
                    'team name TD', 'team name TD2', 'A', 2.6, 3.1, 3.2, 2, 4))
            db.upsert(Match(201809051, '2018-09-05', 'league mnemonic TD', \
                    'team name TD', 'team name TD2', 'H', 2.6, 3.1, 3.2, 2, 1))
            db.upsert(Match(201809061, '2018-09-06', 'league mnemonic TD', \
                    'team name TD', 'team name TD2', 'D', 2.6, 3.1, 3.2, 3, 3))
            db.upsert(Match(201809071, '2018-09-07', 'league mnemonic TD', \
                    'team name TD', 'team name TD2', 'H', 2.6, 3.1, 3.2, 1, 0))

    def setUp(self):
        createName = './db/createdb.sql' 
        testDataName = './db/dbos/*_data.sql' 
        self.dbName = './db/test.db'
        instaticName = './db/instatic.sql'
        insourcesName = './db/insources.sql'
        os.system('cat {} | sqlite3 {}'.format(createName, self.dbName))
        os.system('cat {} | sqlite3 {}'.format(testDataName, self.dbName))
        os.system('cat {} | sqlite3 {}'.format(instaticName, self.dbName))
        os.system('cat {} | sqlite3 {}'.format(insourcesName, self.dbName))

        self.mock_Logger = MagicMock()
        self.mockGlobals()
        self.initialiseData()

    def tearDown(self):
        self.resetGlobals()

    def test_analyseMatches(self):
        analyseMatches(self.mock_Logger, 1, 'league mnemonic TD')

        calls = (
                    call.info('Analysing matches for league <league ' \
                            'mnemonic TD> with algo <1>'),
                    call.debug('Opening database: ./db/test.db'),
                    call.debug('Last rating for match 99'),
                    call.debug('7 matches found to mark'),
                )
        self.mock_Logger.assert_has_calls(calls)

        with Database(self.dbName, SQLite3Impl()) as db:
            stats = db.select(Statistics())
            ratings = db.select(Rating())

            self.assertEquals(len(stats), 2)
            self.assertEquals(stats[0].getGeneration_Date(), \
                    str(datetime.now().date()))
            self.assertEquals(stats[0].getAlgo_Id(), 1)
            self.assertEquals(stats[0].getLeague(), 'league mnemonic TD')
            self.assertEquals(stats[0].getMark(), -3)
            self.assertEquals(stats[0].getMark_Freq(), 50.0)
            self.assertEquals(stats[0].getHome_Freq(), 100.0)
            self.assertEquals(stats[0].getAway_Freq(), 0.0)
            self.assertEquals(stats[0].getDraw_Freq(), 0.0)

            self.assertEquals(stats[1].getGeneration_Date(), \
                    str(datetime.now().date()))
            self.assertEquals(stats[1].getAlgo_Id(), 1)
            self.assertEquals(stats[1].getLeague(), 'league mnemonic TD')
            self.assertEquals(stats[1].getMark(), -2)
            self.assertEquals(stats[1].getMark_Freq(), 50.0)
            self.assertEquals(stats[1].getHome_Freq(), 100.0)
            self.assertEquals(stats[1].getAway_Freq(), 0.0)
            self.assertEquals(stats[1].getDraw_Freq(), 0.0)

            self.assertEquals(len(ratings), 2)
            self.assertEquals(ratings[0].getMatch_Oid(), 6)
            self.assertEquals(ratings[0].getAlgo_Id(), 1)
            self.assertEquals(ratings[0].getMark(), -3)

            self.assertEquals(ratings[1].getMatch_Oid(), 7)
            self.assertEquals(ratings[1].getAlgo_Id(), 1)
            self.assertEquals(ratings[1].getMark(), -2)

if __name__ == '__main__':
    import unittest
    unittest.main()
