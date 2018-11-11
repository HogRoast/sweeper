# coding: utf-8

import configparser, sys, csv, os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call

from shimbase.database import Database, AdhocKeys
from shimbase.sqlite3impl import SQLite3Impl
from sweeper.dbos.match import Match
from sweeper.dbos.team import Team
from sweeper.dbos.source_season_map import Source_Season_Map
from sourcedata import sourceData, getBestOdds

class TestSourceData(TestCase):
    """SourceData tests"""

    def mock_getSweeperConfig(self):
        baseCfg = {'dbName' : './db/test.db'}
        return baseCfg

    def mockGlobals(self):
        self.orig_getSweeperConfig = sourceData.__globals__['getSweeperConfig']
        self.orig_Logger = sourceData.__globals__['Logger']
        self.orig_readCSVFileAsDict = \
                sourceData.__globals__['readCSVFileAsDict']

        sourceData.__globals__['getSweeperConfig'] = self.mock_getSweeperConfig
        sourceData.__globals__['Logger'] = self.mock_Logger
        sourceData.__globals__['readCSVFileAsDict'] = \
                self.mock_readCSVFileAsDict

    def resetGlobals(self):
        sourceData.__globals__['getSweeperConfig'] = self.orig_getSweeperConfig
        sourceData.__globals__['Logger'] = self.orig_Logger
        sourceData.__globals__['readCSVFileAsDict'] = \
                self.orig_readCSVFileAsDict

    def mock_csvData__iter__(self, other):
        return self.csv_data.__iter__()

    def mock_csvData__next__(self, other):
        return self.csv_data.__next__()

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

        self.csv_data = [dict([('b"Div', 'E1'), ('Date', '19/10/10'), ('HomeTeam', 'Coventry'), ('AwayTeam', 'Cardiff'), ('FTHG', '1'), ('FTAG', '2'), ('FTR', 'A'), ('HTHG', '1'), ('HTAG', '1'), ('HTR', 'D'), ('Referee', 'J Linington'), ('HS', '12'), ('AS', '9'), ('HST', '5'), ('AST', '6'), ('HF', '12'), ('AF', '10'), ('HC', '5'), ('AC', '4'), ('HY', '2'), ('AY', '0'), ('HR', '0'), ('AR', '0'), ('B365H', '2.88'), ('B365D', '3.3'), ('B365A', '2.4'), ('BWH', '2.75'), ('BWD', '3.2'), ('BWA', '2.3'), ('GBH', '2.9'), ('GBD', '3.25'), ('GBA', '2.3'), ('IWH', '2.5'), ('IWD', '3.1'), ('IWA', '2.4'), ('LBH', '2.88'), ('LBD', '3.3'), ('LBA', '2.4'), ('SBH', '2.9'), ('SBD', '3.1'), ('SBA', '2.3'), ('WHH', '3.1'), ('WHD', '3.1'), ('WHA', '2.38'), ('SJH', '2.8'), ('SJD', '3.25'), ('SJA', '2.4'), ('VCH', '3.12'), ('VCD', '3.4'), ('VCA', '2.38'), ('BSH', '2.9'), ('BSD', '3.3'), ('BSA', '2.3'), ('Bb1X2', '36'), ('BbMxH', '3.22'), ('BbAvH', '2.94'), ('BbMxD', '3.44'), ('BbAvD', '3.26'), ('BbMxA', '2.4'), ('BbAvA', '2.34'), ('BbOU', '35'), ('BbMx>2.5', '2.07'), ('BbAv>2.5', '1.98'), ('BbMx<2.5', '1.87'), ('BbAv<2.5', '1.78'), ('BbAH', '23'), ('BbAHh', '0'), ('BbMxAHH', '2.27'), ('BbAvAHH', '2.16'), ('BbMxAHA', '1.72'), ('BbAvAHA', '1.66')])]
        self.mock_Logger = MagicMock()
        self.mock_readCSVFileAsDict = MagicMock()
        self.mock_readCSVFileAsDict().__enter__().__iter__ = \
                self.mock_csvData__iter__
        self.mock_readCSVFileAsDict().__enter__().__next__ = \
                self.mock_csvData__next__

        self.mockGlobals()

    def tearDown(self):
        self.resetGlobals()

    def test_getBestOdds(self):
        row = dict([('b"Div', 'E1'), ('Date', '19/10/10'), ('HomeTeam', 'Coventry'), ('AwayTeam', 'Cardiff'), ('FTHG', '1'), ('FTAG', '2'), ('FTR', 'A'), ('HTHG', '1'), ('HTAG', '1'), ('HTR', 'D'), ('Referee', 'J Linington'), ('HS', '12'), ('AS', '9'), ('HST', '5'), ('AST', '6'), ('HF', '12'), ('AF', '10'), ('HC', '5'), ('AC', '4'), ('HY', '2'), ('AY', '0'), ('HR', '0'), ('AR', '0'), ('B365H', '2.88'), ('B365D', '3.3'), ('B365A', '2.4'), ('BWH', '2.75'), ('BWD', '3.2'), ('BWA', '2.3'), ('GBH', '2.9'), ('GBD', '3.25'), ('GBA', '2.3'), ('IWH', '2.5'), ('IWD', '3.1'), ('IWA', '2.4'), ('LBH', '2.88'), ('LBD', '3.3'), ('LBA', '2.4'), ('SBH', '2.9'), ('SBD', '3.1'), ('SBA', '2.3'), ('WHH', '3.1'), ('WHD', '3.1'), ('WHA', '2.38'), ('SJH', '2.8'), ('SJD', '3.25'), ('SJA', '2.4'), ('VCH', '3.12'), ('VCD', '3.4'), ('VCA', '2.38'), ('BSH', '2.9'), ('BSD', '3.3'), ('BSA', '2.3'), ('Bb1X2', '36'), ('BbMxH', '3.22'), ('BbAvH', '2.94'), ('BbMxD', '3.44'), ('BbAvD', '3.26'), ('BbMxA', '2.4'), ('BbAvA', '2.34'), ('BbOU', '35'), ('BbMx>2.5', '2.07'), ('BbAv>2.5', '1.98'), ('BbMx<2.5', '1.87'), ('BbAv<2.5', '1.78'), ('BbAH', '23'), ('BbAHh', '0'), ('BbMxAHH', '2.27'), ('BbAvAHH', '2.16'), ('BbMxAHA', '1.72'), ('BbAvAHA', '1.66')])
        odds = getBestOdds(self.mock_Logger, row)
        self.assertEqual(odds, (3.12, 3.4, 2.4))

        row = dict([('b"Div', 'E1'), ('Date', '19/10/10'), ('HomeTeam', 'Coventry'), ('AwayTeam', 'Cardiff'), ('FTHG', '1'), ('FTAG', '2'), ('FTR', 'A'), ('HTHG', '1'), ('HTAG', '1'), ('HTR', 'D'), ('Referee', 'J Linington'), ('HS', '12'), ('AS', '9'), ('HST', '5'), ('AST', '6'), ('HF', '12'), ('AF', '10'), ('HC', '5'), ('AC', '4'), ('HY', '2'), ('AY', '0'), ('HR', '0'), ('AR', '0'), ('B365H', '2.88'), ('B365D', '3.3'), ('BWH', '2.75'), ('BWD', '3.2'), ('BWA', '2.3'), ('GBH', '2.9'), ('GBD', '3.25'), ('GBA', '2.3'), ('IWH', '2.5'), ('IWD', '3.1'), ('IWA', '2.4'), ('LBH', '2.88'), ('LBD', '3.3'), ('LBA', '2.4'), ('SBH', '2.9'), ('SBD', '3.1'), ('SBA', '2.3'), ('WHH', '3.1'), ('WHD', '3.1'), ('WHA', '2.38'), ('SJH', '2.8'), ('SJD', '3.25'), ('SJA', '2.4'), ('VCH', '3.12'), ('VCD', '3.4'), ('VCA', '2.38'), ('BSH', '2.9'), ('BSD', '3.3'), ('BSA', '2.3'), ('Bb1X2', '36'), ('BbMxH', '3.22'), ('BbAvH', '2.94'), ('BbMxD', '3.44'), ('BbAvD', '3.26'), ('BbMxA', '2.4'), ('BbAvA', '2.34'), ('BbOU', '35'), ('BbMx>2.5', '2.07'), ('BbAv>2.5', '1.98'), ('BbMx<2.5', '1.87'), ('BbAv<2.5', '1.78'), ('BbAH', '23'), ('BbAHh', '0'), ('BbMxAHH', '2.27'), ('BbAvAHH', '2.16'), ('BbMxAHA', '1.72'), ('BbAvAHA', '1.66')])
        odds = getBestOdds(self.mock_Logger, row)
        self.assertEqual(odds, (3.12, 3.4, 2.4))

        row = dict([('b"Div', 'E1'), ('Date', '19/10/10'), ('HomeTeam', 'Coventry'), ('AwayTeam', 'Cardiff'), ('FTHG', '1'), ('FTAG', '2'), ('FTR', 'A'), ('HTHG', '1'), ('HTAG', '1'), ('HTR', 'D'), ('Referee', 'J Linington'), ('HS', '12'), ('AS', '9'), ('HST', '5'), ('AST', '6'), ('HF', '12'), ('AF', '10'), ('HC', '5'), ('AC', '4'), ('HY', '2'), ('AY', '0'), ('HR', '0'), ('AR', '0'), ('B365H', '2.88'), ('B365D', '3.3'), ('B365A', '2.4'), ('BWD', '3.2'), ('BWA', '2.3'), ('GBH', '2.9'), ('GBD', '3.25'), ('GBA', '2.3'), ('IWH', '2.5'), ('IWD', '3.1'), ('IWA', '2.4'), ('LBH', '2.88'), ('LBD', '3.3'), ('LBA', '2.4'), ('SBH', '2.9'), ('SBD', '3.1'), ('SBA', '2.3'), ('WHH', '3.1'), ('WHD', '3.1'), ('WHA', '2.38'), ('SJH', '2.8'), ('SJD', '3.25'), ('SJA', '2.4'), ('VCH', '3.12'), ('VCD', '3.4'), ('VCA', '2.38'), ('BSH', '2.9'), ('BSD', '3.3'), ('BSA', '2.3'), ('Bb1X2', '36'), ('BbMxH', '3.22'), ('BbAvH', '2.94'), ('BbMxD', '3.44'), ('BbAvD', '3.26'), ('BbMxA', '2.4'), ('BbAvA', '2.34'), ('BbOU', '35'), ('BbMx>2.5', '2.07'), ('BbAv>2.5', '1.98'), ('BbMx<2.5', '1.87'), ('BbAv<2.5', '1.78'), ('BbAH', '23'), ('BbAHh', '0'), ('BbMxAHH', '2.27'), ('BbAvAHH', '2.16'), ('BbMxAHA', '1.72'), ('BbAvAHA', '1.66')])
        odds = getBestOdds(self.mock_Logger, row)
        self.assertEqual(odds, (3.12, 3.4, 2.4))

        row = dict([('b"Div', 'E1'), ('Date', '19/10/10'), ('HomeTeam', 'Coventry'), ('AwayTeam', 'Cardiff'), ('FTHG', '1'), ('FTAG', '2'), ('FTR', 'A'), ('HTHG', '1'), ('HTAG', '1'), ('HTR', 'D'), ('Referee', 'J Linington'), ('HS', '12'), ('AS', '9'), ('HST', '5'), ('AST', '6'), ('HF', '12'), ('AF', '10'), ('HC', '5'), ('AC', '4'), ('HY', '2'), ('AY', '0'), ('HR', '0'), ('AR', '0'), ('B365H', '2.88'), ('B365D', '3.3'), ('B365A', '2.4'), ('BWH', '2.75'), ('BWD', '3.2'), ('BWA', '2.3'), ('GBH', '2.9'), ('GBD', '3.25'), ('GBA', '2.3'), ('IWH', '2.5'), ('IWD', '3.1'), ('LBH', '2.88'), ('LBD', '3.3'), ('LBA', '2.4'), ('SBH', '2.9'), ('SBD', '3.1'), ('SBA', '2.3'), ('WHH', '3.1'), ('WHD', '3.1'), ('WHA', '2.38'), ('SJH', '2.8'), ('SJD', '3.25'), ('SJA', '2.4'), ('VCH', '3.12'), ('VCD', '3.4'), ('VCA', '2.38'), ('BSH', '2.9'), ('BSD', '3.3'), ('BSA', '2.3'), ('Bb1X2', '36'), ('BbMxH', '3.22'), ('BbAvH', '2.94'), ('BbMxD', '3.44'), ('BbAvD', '3.26'), ('BbMxA', '2.4'), ('BbAvA', '2.34'), ('BbOU', '35'), ('BbMx>2.5', '2.07'), ('BbAv>2.5', '1.98'), ('BbMx<2.5', '1.87'), ('BbAv<2.5', '1.78'), ('BbAH', '23'), ('BbAHh', '0'), ('BbMxAHH', '2.27'), ('BbAvAHH', '2.16'), ('BbMxAHA', '1.72'), ('BbAvAHA', '1.66')])
        odds = getBestOdds(self.mock_Logger, row)
        self.assertEqual(odds, (3.12, 3.4, 2.4))

        row = dict([('b"Div', 'E1'), ('Date', '19/10/10'), ('HomeTeam', 'Coventry'), ('AwayTeam', 'Cardiff'), ('FTHG', '1'), ('FTAG', '2'), ('FTR', 'A'), ('HTHG', '1'), ('HTAG', '1'), ('HTR', 'D'), ('Referee', 'J Linington'), ('HS', '12'), ('AS', '9'), ('HST', '5'), ('AST', '6'), ('HF', '12'), ('AF', '10'), ('HC', '5'), ('AC', '4'), ('HY', '2'), ('AY', '0'), ('HR', '0'), ('AR', '0'), ('B365H', '2.88'), ('B365D', '3.3'), ('B365A', '2.4'), ('BWH', '2.75'), ('BWD', '3.2'), ('BWA', '2.3'), ('GBH', '2.9'), ('GBD', '3.25'), ('GBA', '2.3'), ('IWH', '2.5'), ('IWD', '3.1'), ('IWA', '2.4'), ('LBD', '3.3'), ('LBA', '2.4'), ('SBH', '2.9'), ('SBD', '3.1'), ('SBA', '2.3'), ('WHH', '3.1'), ('WHD', '3.1'), ('WHA', '2.38'), ('SJH', '2.8'), ('SJD', '3.25'), ('SJA', '2.4'), ('VCH', '3.12'), ('VCD', '3.4'), ('VCA', '2.38'), ('BSH', '2.9'), ('BSD', '3.3'), ('BSA', '2.3'), ('Bb1X2', '36'), ('BbMxH', '3.22'), ('BbAvH', '2.94'), ('BbMxD', '3.44'), ('BbAvD', '3.26'), ('BbMxA', '2.4'), ('BbAvA', '2.34'), ('BbOU', '35'), ('BbMx>2.5', '2.07'), ('BbAv>2.5', '1.98'), ('BbMx<2.5', '1.87'), ('BbAv<2.5', '1.78'), ('BbAH', '23'), ('BbAHh', '0'), ('BbMxAHH', '2.27'), ('BbAvAHH', '2.16'), ('BbMxAHA', '1.72'), ('BbAvAHA', '1.66')])
        odds = getBestOdds(self.mock_Logger, row)
        self.assertEqual(odds, (3.12, 3.4, 2.4))

        row = dict([('b"Div', 'E1'), ('Date', '19/10/10'), ('HomeTeam', 'Coventry'), ('AwayTeam', 'Cardiff'), ('FTHG', '1'), ('FTAG', '2'), ('FTR', 'A'), ('HTHG', '1'), ('HTAG', '1'), ('HTR', 'D'), ('Referee', 'J Linington'), ('HS', '12'), ('AS', '9'), ('HST', '5'), ('AST', '6'), ('HF', '12'), ('AF', '10'), ('HC', '5'), ('AC', '4'), ('HY', '2'), ('AY', '0'), ('HR', '0'), ('AR', '0'), ('B365H', '2.88'), ('B365D', '3.3'), ('B365A', '2.4'), ('BWH', '2.75'), ('BWD', '3.2'), ('BWA', '2.3'), ('GBH', '2.9'), ('GBD', '3.25'), ('GBA', '2.3'), ('IWH', '2.5'), ('IWD', '3.1'), ('IWA', '2.4'), ('LBH', '2.88'), ('LBD', '3.3'), ('LBA', '2.4'), ('SBH', '2.9'), ('SBD', '3.1'), ('SBA', '2.3'), ('WHD', '3.1'), ('WHA', '2.38'), ('SJH', '2.8'), ('SJD', '3.25'), ('SJA', '2.4'), ('VCH', '3.12'), ('VCD', '3.4'), ('VCA', '2.38'), ('BSH', '2.9'), ('BSD', '3.3'), ('BSA', '2.3'), ('Bb1X2', '36'), ('BbMxH', '3.22'), ('BbAvH', '2.94'), ('BbMxD', '3.44'), ('BbAvD', '3.26'), ('BbMxA', '2.4'), ('BbAvA', '2.34'), ('BbOU', '35'), ('BbMx>2.5', '2.07'), ('BbAv>2.5', '1.98'), ('BbMx<2.5', '1.87'), ('BbAv<2.5', '1.78'), ('BbAH', '23'), ('BbAHh', '0'), ('BbMxAHH', '2.27'), ('BbAvAHH', '2.16'), ('BbMxAHA', '1.72'), ('BbAvAHA', '1.66')])
        odds = getBestOdds(self.mock_Logger, row)
        self.assertEqual(odds, (3.12, 3.4, 2.4))

        row = dict([('b"Div', 'E1'), ('Date', '19/10/10'), ('HomeTeam', 'Coventry'), ('AwayTeam', 'Cardiff'), ('FTHG', '1'), ('FTAG', '2'), ('FTR', 'A'), ('HTHG', '1'), ('HTAG', '1'), ('HTR', 'D'), ('Referee', 'J Linington'), ('HS', '12'), ('AS', '9'), ('HST', '5'), ('AST', '6'), ('HF', '12'), ('AF', '10'), ('HC', '5'), ('AC', '4'), ('HY', '2'), ('AY', '0'), ('HR', '0'), ('AR', '0'), ('B365H', '2.88'), ('B365D', '3.3'), ('B365A', '2.4'), ('BWH', '2.75'), ('BWD', '3.2'), ('BWA', '2.3'), ('GBH', '2.9'), ('GBD', '3.25'), ('GBA', '2.3'), ('IWH', '2.5'), ('IWD', '3.1'), ('IWA', '2.4'), ('LBH', '2.88'), ('LBD', '3.3'), ('LBA', '2.4'), ('SBH', '2.9'), ('SBD', '3.1'), ('SBA', '2.3'), ('WHH', '3.1'), ('WHD', '3.1'), ('WHA', '2.38'), ('SJH', '2.8'), ('SJD', '3.25'), ('SJA', '2.4'), ('VCD', '3.4'), ('VCA', '2.38'), ('BSH', '2.9'), ('BSD', '3.3'), ('BSA', '2.3'), ('Bb1X2', '36'), ('BbMxH', '3.22'), ('BbAvH', '2.94'), ('BbMxD', '3.44'), ('BbAvD', '3.26'), ('BbMxA', '2.4'), ('BbAvA', '2.34'), ('BbOU', '35'), ('BbMx>2.5', '2.07'), ('BbAv>2.5', '1.98'), ('BbMx<2.5', '1.87'), ('BbAv<2.5', '1.78'), ('BbAH', '23'), ('BbAHh', '0'), ('BbMxAHH', '2.27'), ('BbAvAHH', '2.16'), ('BbMxAHA', '1.72'), ('BbAvAHA', '1.66')])
        odds = getBestOdds(self.mock_Logger, row)
        self.assertEqual(odds, (3.1, 3.3, 2.4))

        calls = (
                    call.debug(
                        'No B365 data - skipping : 19/10/10 Coventry Cardiff'),
                    call.debug(
                        'No BW data - skipping : 19/10/10 Coventry Cardiff'),
                    call.debug(
                        'No IW data - skipping : 19/10/10 Coventry Cardiff'),
                    call.debug(
                        'No WH data - skipping : 19/10/10 Coventry Cardiff'),
                    call.debug(
                        'No VC data - skipping : 19/10/10 Coventry Cardiff')
                )
        self.mock_Logger.assert_has_calls(calls)

    def test_sourceData(self):
        with Database(self.dbName, SQLite3Impl()) as db, \
                db.transaction() as t:
            seasonMap = db.select(Source_Season_Map(98))[0]
            seasonMap.setActive(1)
            db.upsert(seasonMap)

        sourceData(self.mock_Logger, 'source name TD', False)

        self.mock_readCSVFileAsDict.assert_any_call( \
                'source_season_map data_url TD')

        calls = (
                    call.info(
                        'Downloading data from source: source name TD'),
                    call.debug('Opening database: ./db/test.db'),
                    call.debug(
                        "source : Keys {'id': 98} : Values {'name': " \
                        "'source name TD', 'fixtures_url': 'source " \
                        "fixtures_url TD', 'url': 'source url TD'}"),
                    call.debug(
                        "[source_season_map : Keys {'source_id': 98, "\
                        "'season': 'season name TD'} : Values {'moniker'" \
                        ": 'source_season_map moniker TD', 'data_url': " \
                        "'source_season_map data_url TD', 'active': 1}]"),
                    call.debug(
                        "[source_league_map : Keys {'source_id': 98, " \
                        "'league': 'league mnemonic TD'} : Values " \
                        "{'moniker': 'source_league_map moniker TD'}]"),
                    call.debug(
                        "[team : Keys {'name': 'team name TD'} : Values " \
                        "{'league': 'league mnemonic TD'}, " \
                        "team : Keys {'name': 'team name TD2'} : Values " \
                        "{'league': 'league mnemonic TD2'}]"),
                    call.info('Downloading...source_season_map data_url TD'),
                )
        self.mock_Logger.assert_has_calls(calls)

        with Database(self.dbName, SQLite3Impl()) as db:
            ht = db.select(Team('Coventry', 'league mnemonic TD'))[0]
            at = db.select(Team('Cardiff', 'league mnemonic TD'))[0]
            match = db.select(Match(201010191))[0]

            self.assertTrue(ht and at and match)
            self.assertEquals(match.getDate(), '2010-10-19')
            self.assertEquals(match.getLeague(), 'league mnemonic TD')
            self.assertEquals(match.getHome_Team(), 'Coventry')
            self.assertEquals(match.getAway_Team(), 'Cardiff')
            self.assertEquals(match.getResult(), 'A')
            self.assertEquals(match.getBest_Odds_H(), 3.12)
            self.assertEquals(match.getBest_Odds_D(), 3.4)
            self.assertEquals(match.getBest_Odds_A(), 2.4)
            self.assertEquals(match.getHome_Goals(), 1)
            self.assertEquals(match.getAway_Goals(), 2)
            self.assertEquals(match.getHome_Lp(), None)
            self.assertEquals(match.getAway_Lp(), None)

    def test_sourceData_CurrentSeason(self):
        with Database(self.dbName, SQLite3Impl()) as db, \
                db.transaction() as t:
            seasonMap = db.select(Source_Season_Map(98))[0]
            seasonMap.setActive(1)
            db.upsert(seasonMap)
            seasonMap = Source_Season_Map(98, 'season name TD2', \
                    'source_season_map moniker TD2', \
                    'source_season_map data_url TD2', 1)
            db.upsert(seasonMap)

        sourceData(self.mock_Logger, 'source name TD', True)

        self.mock_readCSVFileAsDict.assert_any_call( \
                'source_season_map data_url TD2')

        calls = (
                    call.info(
                        'Downloading data from source: source name TD'),
                    call.debug('Opening database: ./db/test.db'),
                    call.debug(
                        "source : Keys {'id': 98} : Values {'name': " \
                        "'source name TD', 'fixtures_url': 'source " \
                        "fixtures_url TD', 'url': 'source url TD'}"),
                    call.debug(
                        "[source_season_map : Keys {'source_id': 98, "\
                        "'season': 'season name TD2'} : Values {'moniker'" \
                        ": 'source_season_map moniker TD2', 'data_url': " \
                        "'source_season_map data_url TD2', 'active': 1}]"),
                    call.debug(
                        "[source_league_map : Keys {'source_id': 98, " \
                        "'league': 'league mnemonic TD'} : Values " \
                        "{'moniker': 'source_league_map moniker TD'}]"),
                    call.debug(
                        "[team : Keys {'name': 'team name TD'} : Values " \
                        "{'league': 'league mnemonic TD'}, " \
                        "team : Keys {'name': 'team name TD2'} : Values " \
                        "{'league': 'league mnemonic TD2'}]"),
                    call.info('Downloading...source_season_map data_url TD2'),
                )
        self.mock_Logger.assert_has_calls(calls)

        with Database(self.dbName, SQLite3Impl()) as db:
            ht = db.select(Team('Coventry', 'league mnemonic TD'))[0]
            at = db.select(Team('Cardiff', 'league mnemonic TD'))[0]
            match = db.select(Match(201010191))[0]

            self.assertTrue(ht and at and match)
            self.assertEquals(match.getDate(), '2010-10-19')
            self.assertEquals(match.getLeague(), 'league mnemonic TD')
            self.assertEquals(match.getHome_Team(), 'Coventry')
            self.assertEquals(match.getAway_Team(), 'Cardiff')
            self.assertEquals(match.getResult(), 'A')
            self.assertEquals(match.getBest_Odds_H(), 3.12)
            self.assertEquals(match.getBest_Odds_D(), 3.4)
            self.assertEquals(match.getBest_Odds_A(), 2.4)
            self.assertEquals(match.getHome_Goals(), 1)
            self.assertEquals(match.getAway_Goals(), 2)
            self.assertEquals(match.getHome_Lp(), None)
            self.assertEquals(match.getAway_Lp(), None)

if __name__ == '__main__':
    import unittest
    unittest.main()
