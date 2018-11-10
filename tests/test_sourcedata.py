# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, sys, csv, os
from sourcedata import sourceData, getBestOdds

class TestSourceData(TestCase):
    """SourceData tests"""

    @classmethod
    def setUpClass(cls):
        createName = './db/createdb.sql' 
        testDataName = './db/dbos/*_data.sql' 
        dbName = './db/test.db'
        instaticName = './db/instatic.sql'
        insourcesName = './db/insources.sql'
        os.system('cat {} | sqlite3 {}'.format(createName, dbName))
        os.system('cat {} | sqlite3 {}'.format(testDataName, dbName))
        os.system('cat {} | sqlite3 {}'.format(instaticName, dbName))
        os.system('cat {} | sqlite3 {}'.format(insourcesName, dbName))

    @classmethod
    def tearDownClass(cls):
        pass

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
                        'No LB data - skipping : 19/10/10 Coventry Cardiff'),
                    call.debug(
                        'No WH data - skipping : 19/10/10 Coventry Cardiff'),
                    call.debug(
                        'No VC data - skipping : 19/10/10 Coventry Cardiff')
                )
        self.mock_Logger.assert_has_calls(calls)

    def test_sourceData(self):
        '''
        sourceData('Football-Data', ['test', '-d'])

        args = (
                    urlTmpl.format('1718', 'E0'),
                    urlTmpl.format('1617', 'E0'),
                    urlTmpl.format('1718', 'D1'),
                    urlTmpl.format('1617', 'D1'),
                )
        for a in args:
            self.mock_readCSVFileAsDict.assert_any_call(a)

        line1 = self.csv_data[0]
        line1[0] = 'Div'
        line2 = self.csv_data[1]
        calls = (
                    call(outFile.format('E0', '1718'), line1),
                    call().__enter__(),
                    call().__enter__().writerow(line2),
                    call().__exit__(None, None, None),
                    call(outFile.format('E0', '1617'), line1),
                    call().__enter__(),
                    call().__enter__().writerow(line2),
                    call().__exit__(None, None, None),
                    call(outFile.format('D1', '1718'), line1),
                    call().__enter__(),
                    call().__enter__().writerow(line2),
                    call().__exit__(None, None, None),
                    call(outFile.format('D1', '1617'), line1),
                    call().__enter__(),
                    call().__enter__().writerow(line2),
                    call().__exit__(None, None, None),
                )
        self.mock_newCSVFile.assert_has_calls(calls)
        '''

if __name__ == '__main__':
    import unittest
    unittest.main()
