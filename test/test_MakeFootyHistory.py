# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, pprint, csv
import urllib.request
from Footy.src.MakeFootyHistory import makeFootyHistory 

class TestMakeFootyHistory(TestCase):
    """MakeFootyHistory tests"""

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
        self.orig_getFootyConfig = makeFootyHistory.__globals__['getFootyConfig']
        self.orig_newCSVFile = makeFootyHistory.__globals__['newCSVFile']
        self.orig_Logger = makeFootyHistory.__globals__['Logger']
        self.orig_urlopen = makeFootyHistory.__globals__['urllib'].request.urlopen
        self.orig_csv_reader = makeFootyHistory.__globals__['csv'].DictReader
        self.orig_model = makeFootyHistory.__globals__['model']
        self.orig_stats = makeFootyHistory.__globals__['stats']

        makeFootyHistory.__globals__['getFootyConfig'] = self.mock_getFootyConfig
        makeFootyHistory.__globals__['newCSVFile'] = self.mock_newCSVFile
        makeFootyHistory.__globals__['Logger'] = self.mock_Logger
        makeFootyHistory.__globals__['urllib'].request.urlopen = self.mock_urlopen
        makeFootyHistory.__globals__['csv'].DictReader = self.mock_csv_reader
        makeFootyHistory.__globals__['model'] = self.mock_model
        makeFootyHistory.__globals__['stats'] = self.mock_stats

    def resetGlobals(self):
        makeFootyHistory.__globals__['getFootyConfig'] = self.orig_getFootyConfig
        makeFootyHistory.__globals__['newCSVFile'] = self.orig_newCSVFile
        makeFootyHistory.__globals__['Logger'] = self.orig_Logger
        makeFootyHistory.__globals__['urllib'].request.urlopen = self.orig_urlopen
        makeFootyHistory.__globals__['csv'].DictReader = self.orig_csv_reader
        makeFootyHistory.__globals__['model'] = self.orig_model
        makeFootyHistory.__globals__['stats'] = self.orig_stats

    def setUp(self):
        self.mock_newCSVFile = MagicMock()
        self.mock_Logger = MagicMock()
        self.mock_urlopen = MagicMock(spec=urllib.request.urlopen)
        
        self.mock_open = MagicMock(
                spec=open, return_Value = 'return from mock open')
        self.mock_csv_reader = MagicMock(
                spec=csv.DictReader, 
                return_value = [{
                    'Date' : '27/09/17', 
                    'HomeTeam' : 'Arsenal',
                    'AwayTeam' : 'Chelsea', 
                    'FTR' : 'H'}])

        self.mock_urlopen().read = MagicMock(
                return_value = 'return from mock urlopen.read')

        self.mock_model = MagicMock(spec=['processMatches', 'markMatch'])
        self.mock_model.processMatches = MagicMock(
                return_value = 'return from mock processMatches')
        self.mock_model.markMatch = MagicMock(return_value = (
                '01/01/2018', 'Chelsea', 'Arsenal', 0, 'W:3v0', 'L:2v1'))

        self.mock_stats = MagicMock(spec=['linregress'])
        self.mock_stats.linregress = MagicMock(
                return_value = (50.0, 10.0, 0.5, 0.45, 0.24))

        self.mockGlobals()

    def tearDown(self):
        self.resetGlobals()

    def test_makeFootyHistory(self):
        urlTmpl = 'http://test.com/{}/{}.csv'
        makeFootyHistory(urlTmpl, [])
        
        self.mock_Logger().info.assert_any_call(
                'Footy.src.MakeFootyHistory : MagicMock')
        self.mock_Logger().info.assert_any_call('League : E0...')
        self.mock_Logger().info.assert_any_call('League : D1...')
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/E0/History.MagicMock.csv',
                ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result'])
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/D1/History.MagicMock.csv',
                ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result'])

        tmp = urlTmpl.format('1718', 'E0')
        self.mock_Logger().debug.assert_any_call('Processing...' + tmp)
        self.mock_urlopen.assert_any_call(tmp)
        tmp = urlTmpl.format('1617', 'E0')
        self.mock_Logger().debug.assert_any_call('Processing...' + tmp)
        self.mock_urlopen.assert_any_call(tmp)
        tmp = urlTmpl.format('1718', 'D1')
        self.mock_Logger().debug.assert_any_call('Processing...' + tmp)
        self.mock_urlopen.assert_any_call(tmp)
        tmp = urlTmpl.format('1617', 'D1')
        self.mock_Logger().debug.assert_any_call('Processing...' + tmp)
        self.mock_urlopen.assert_any_call(tmp)
 
        self.mock_model.processMatches.assert_any_call(
                [{'Date' : '27/09/17', 
                  'HomeTeam' : 'Arsenal',
                  'AwayTeam' : 'Chelsea', 
                  'FTR' : 'H'}])
        self.mock_model.markMatch.assert_any_call(
                'return from mock processMatches', '27/09/17', 
                'Arsenal', 'Chelsea')
        self.mock_newCSVFile().__enter__().writerow.assert_any_call([
                '01/01/2018', 'Chelsea', 'Arsenal', 0, 'H'])

        self.mock_Logger().info.assert_any_call('Writing summary data...')
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/D1/Summary.MagicMock.csv',
                ['Mark', 'Frequency', '%H','HO', '%D', 'DO', '%A', 'AO'])
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/D1/Summary.MagicMock.csv',
                ['Mark', 'Frequency', '%H','HO', '%D', 'DO', '%A', 'AO'])
        self.mock_newCSVFile().__enter__().writerow.assert_any_call([
                0, 2, '100.00', '1.00', '0.00', '0.00', '0.00', '0.00'])

        self.mock_Logger().info.assert_any_call('0 (2 100.00) ')
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/D1/Stats.MagicMock.csv',
                ['Result', 'Slope', 'Intercept', 'P', 'R', 'R^2', 'Err'])
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/D1/Stats.MagicMock.csv',
                ['Result', 'Slope', 'Intercept', 'P', 'R', 'R^2', 'Err'])
        self.mock_stats.linregress.assert_any_call([0], [100.0])
        self.mock_stats.linregress.assert_any_call([0], [0.0])
        self.mock_Logger().info.assert_any_call('Home: 50.00 10.00 0.45 0.50 0.25 0.24')
        self.mock_Logger().info.assert_any_call('Draw: 50.00 10.00 0.45 0.50 0.25 0.24')
        self.mock_Logger().info.assert_any_call('Away: 50.00 10.00 0.45 0.50 0.25 0.24')

        self.mock_newCSVFile().__enter__().writerow.assert_any_call([
                'H', '50.00', '10.00', '0.45', '0.50', '0.25', '0.24'])
        self.mock_newCSVFile().__enter__().writerow.assert_any_call([
                'D', '50.00', '10.00', '0.45', '0.50', '0.25', '0.24'])
        self.mock_newCSVFile().__enter__().writerow.assert_any_call([
                'A', '50.00', '10.00', '0.45', '0.50', '0.25', '0.24'])

if __name__ == '__main__':
    import unittest
    unittest.main()
