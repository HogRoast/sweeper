# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, pprint
from Footy.src.FootyBackTest import footyBackTest 

class TestFootyBackTest(TestCase):
    """FootyBackTest tests"""

    def mock_getFootyConfig(self):
        algoCfg = { 
            'seasons' : ['1718', '1617'],
            'rangeMap' : {
                'E0' : range(-1, 2),
                'D1' : range(0, 4)
            }
        }
        mailCfg = None
        return (algoCfg, mailCfg)

    def mockGlobals(self):
        self.orig_getFootyConfig = footyBackTest.__globals__['getFootyConfig']
        self.orig_Logger = footyBackTest.__globals__['Logger']
        self.orig_newCSVFile = footyBackTest.__globals__['newCSVFile']
        self.orig_readCSVFileAsDict = footyBackTest.__globals__['readCSVFileAsDict']
        self.orig_model = footyBackTest.__globals__['model']

        footyBackTest.__globals__['getFootyConfig'] = self.mock_getFootyConfig
        footyBackTest.__globals__['Logger'] = self.mock_Logger
        footyBackTest.__globals__['newCSVFile'] = self.mock_newCSVFile
        footyBackTest.__globals__['readCSVFileAsDict'] = self.mock_readCSVFileAsDict
        footyBackTest.__globals__['model'] = self.mock_model

    def resetGlobals(self):
        footyBackTest.__globals__['getFootyConfig'] = self.orig_getFootyConfig
        footyBackTest.__globals__['Logger'] = self.orig_Logger
        footyBackTest.__globals__['newCSVFile'] = self.orig_newCSVFile
        footyBackTest.__globals__['readCSVFileAsDict'] = self.orig_readCSVFileAsDict
        footyBackTest.__globals__['model'] = self.orig_model

    def mock_csvData__iter__(self, other):
        self.csvCount += 1
        return self.csvData[self.csvCount-1].__iter__()

    def setUp(self):
        self.mock_newCSVFile = MagicMock()
        self.mock_readCSVFileAsDict = MagicMock()
        self.csvData = [[{
                    'Mark' : '0',
                    '%H' : '45.4',
                    'HO' : '2.2',
                    '%D' : '20.3',
                    'DO' : '4.4',
                    '%A' : '34.3',
                    'AO' : '3.3',
                    }],[{
                    'Date' : '27/09/17', 
                    'HomeTeam' : 'Arsenal',
                    'AwayTeam' : 'Chelsea', 
                    'FTR' : 'H',
                    'B365H' : '2.3',
                    'B365D' : '3.4',
                    'B365A' : '2.7',
                    'BWH' : '2.4',
                    'BWD' : '3.4',
                    'BWA' : '2.7',
                    'VCH' : '2.2',
                    'VCD' : '3.4',
                    'VCA' : '2.7',
                    }],[{
                    'Date' : '27/09/17', 
                    'HomeTeam' : 'Arsenal',
                    'AwayTeam' : 'Chelsea', 
                    'FTR' : 'H',
                    'B365H' : '2.3',
                    'B365D' : '3.4',
                    'B365A' : '2.7',
                    'BWH' : '2.4',
                    'BWD' : '3.4',
                    'BWA' : '2.7',
                    'VCH' : '2.2',
                    'VCD' : '3.4',
                    'VCA' : '2.7',
                    }],[{
                    'Mark' : '0',
                    '%H' : '45.4',
                    'HO' : '2.2',
                    '%D' : '20.3',
                    'DO' : '4.4',
                    '%A' : '34.3',
                    'AO' : '3.3',
                    }],[{
                    'Date' : '27/09/17', 
                    'HomeTeam' : 'Arsenal',
                    'AwayTeam' : 'Chelsea', 
                    'FTR' : 'H',
                    'B365H' : '2.3',
                    'B365D' : '3.4',
                    'B365A' : '2.7',
                    'BWH' : '2.4',
                    'BWD' : '3.4',
                    'BWA' : '2.7',
                    'VCH' : '2.2',
                    'VCD' : '3.4',
                    'VCA' : '2.7',
                    }],[{
                    'Date' : '27/09/17', 
                    'HomeTeam' : 'Arsenal',
                    'AwayTeam' : 'Chelsea', 
                    'FTR' : 'H',
                    'B365H' : '2.3',
                    'B365D' : '3.4',
                    'B365A' : '2.7',
                    'BWH' : '2.4',
                    'BWD' : '3.4',
                    'BWA' : '2.7',
                    'VCH' : '2.2',
                    'VCD' : '3.4',
                    'VCA' : '2.7',}]]
        self.csvCount = 0

        self.mock_readCSVFileAsDict().__enter__().__iter__ = \
                self.mock_csvData__iter__
        self.mock_Logger = MagicMock()

        self.mock_model = MagicMock(spec=['processMatches', 'markMatch'])
        self.mock_model.processMatches = MagicMock(
                return_value = 'return from mock processMatches')
        self.mock_model.markMatch = MagicMock(return_value = (
                '01/01/2018', 'Chelsea', 'Arsenal', 0, 'W:3v0', 'L:2v1'))

        self.mockGlobals()

    def tearDown(self):
        self.resetGlobals()

    def test_backtest(self):
        urlTmpl = 'http://test.com/{}/{}.csv'
        footyBackTest(urlTmpl, [])

        self.mock_readCSVFileAsDict.assert_any_call(
                '../Analysis/E0/Summary.MagicMock.csv')
        self.mock_readCSVFileAsDict.assert_any_call(
                '../Analysis/D1/Summary.MagicMock.csv')
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/E0/BackTest.MagicMock.csv',
                ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result', 'MyBet', 
                    'MyOdds', 'Bookie', 'BookieOdds', 'Winnings', 'PnL', 
                    'T_Stk', 'T_W', 'Yield'])
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/D1/BackTest.MagicMock.csv',
                ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result', 'MyBet', 
                    'MyOdds', 'Bookie', 'BookieOdds', 'Winnings', 'PnL', 
                    'T_Stk', 'T_W', 'Yield'])

        tmp = urlTmpl.format('1718', 'E0')
        self.mock_Logger().debug.assert_any_call('Processing...' + tmp)
        self.mock_readCSVFileAsDict.assert_any_call(tmp)
        tmp = urlTmpl.format('1617', 'E0')
        self.mock_Logger().debug.assert_any_call('Processing...' + tmp)
        self.mock_readCSVFileAsDict.assert_any_call(tmp)
        tmp = urlTmpl.format('1718', 'D1')
        self.mock_Logger().debug.assert_any_call('Processing...' + tmp)
        self.mock_readCSVFileAsDict.assert_any_call(tmp)
        tmp = urlTmpl.format('1617', 'D1')
        self.mock_Logger().debug.assert_any_call('Processing...' + tmp)
        self.mock_readCSVFileAsDict.assert_any_call(tmp)

        self.mock_model.processMatches.assert_any_call(
                [{'Date' : '27/09/17', 
                  'HomeTeam' : 'Arsenal',
                  'AwayTeam' : 'Chelsea', 
                  'FTR' : 'H',
                  'B365H' : '2.3',
                  'B365D' : '3.4',
                  'B365A' : '2.7',
                  'BWH' : '2.4',
                  'BWD' : '3.4',
                  'BWA' : '2.7',
                  'VCH' : '2.2',
                  'VCD' : '3.4',
                  'VCA' : '2.7',}])
        self.mock_model.markMatch.assert_any_call(
                'return from mock processMatches', '27/09/17', 
                'Arsenal', 'Chelsea')

        self.mock_Logger().error.assert_any_call(
                'No IW data - skipping : 01/01/2018 Chelsea Arsenal')
        self.mock_Logger().error.assert_any_call(
                'No LB data - skipping : 01/01/2018 Chelsea Arsenal')
        self.mock_Logger().error.assert_any_call(
                'No WH data - skipping : 01/01/2018 Chelsea Arsenal')
 
        self.mock_newCSVFile().__enter__().writerow.assert_any_call(
                ('01/01/2018', 'Chelsea', 'Arsenal', 0, 'H', 'H', 2.2, 'BW', 
                    2.4, 2.4, 1.4, 1, 2.4, 1.4))

        self.mock_Logger().info.assert_any_call(
                'E0    - Staked: GBP  2.00 Won: GBP  4.80 Yield: 140.00%')
        self.mock_Logger().info.assert_any_call(
                'D1    - Staked: GBP  2.00 Won: GBP  4.80 Yield: 140.00%')

if __name__ == '__main__':
    import unittest
    unittest.main()
