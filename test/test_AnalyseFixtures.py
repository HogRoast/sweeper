# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, pprint, csv
import urllib.request
from Footy.src.AnalyseFixtures import analyseFixtures 

class TestAnalyseFixtures(TestCase):
    """AnalyseFixtures tests"""

    def mock_getFootyConfig(self):
        algoCfg = { 
            'seasons' : ['1718', '1617'],
            'rangeMap' : {
                'E0' : range(-1, 2),
                'D1' : range(0, 4)
            }
        }
        mailCfg = {
                'fromAddr' : 'an_email@gmail.com',
                'toAddrs' : """['someone@gmail.com', 
                                'someone_else@gmail.com']""",
                'pwd' : 'password',
                'svr' : 'server123',
                'port' : 1234
                }
        return (algoCfg, mailCfg)

    def mockGlobals(self):
        self.orig_getFootyConfig = analyseFixtures.__globals__['getFootyConfig']
        self.orig_Logger = analyseFixtures.__globals__['Logger']
        self.orig_urlopen = analyseFixtures.__globals__['urllib']
        self.orig_csv_reader = analyseFixtures.__globals__['csv'].DictReader
        self.orig_csv_writer = analyseFixtures.__globals__['csv'].writer
        #self.orig_model = analyseFixtures.__globals__['model']

        analyseFixtures.__globals__['getFootyConfig'] = self.mock_getFootyConfig
        analyseFixtures.__globals__['Logger'] = self.mock_Logger
        analyseFixtures.__globals__['urllib'].request.urlopen = self.mock_urlopen
        analyseFixtures.__globals__['csv'].DictReader = self.mock_csv_reader
        analyseFixtures.__globals__['csv'].writer = self.mock_csv_writer
        #analyseFixtures.__globals__['model'] = self.mock_model

    def resetGlobals(self):
        analyseFixtures.__globals__['getFootyConfig'] = self.orig_getFootyConfig
        analyseFixtures.__globals__['Logger'] = self.orig_Logger
        analyseFixtures.__globals__['urllib'].request.urlopen = self.orig_urlopen
        analyseFixtures.__globals__['csv'].DictReader = self.orig_csv_reader
        analyseFixtures.__globals__['csv'].writer = self.orig_csv_writer
        #analyseFixtures.__globals__['model'] = self.orig_model

    def setUp(self):
        self.mock_Logger = MagicMock()
        self.mock_urlopen = MagicMock(spec=urllib.request.urlopen)
        
        #self.mock_open = MagicMock(
        #        spec=open, return_Value = 'return from mock open')
        self.mock_csv_reader = MagicMock(
                spec=csv.DictReader, 
                return_value = [{
                    'Date' : '27/09/17', 
                    'HomeTeam' : 'Arsenal',
                    'AwayTeam' : 'Chelsea', 
                    'FTR' : 'H'}])
        self.mock_csv_writer = MagicMock(spec=csv.writer)

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

    def test_analyseFixtures(self):
        # TEMPORARY!
        return 

        results = 'http://test.com/{}/{}.csv'
        fixtures = 'http://test.com/fixtures.csv'
        analyseFixtures(results, fixtures)

        self.mock_Logger().info.assert_any_call(
                'src.MakeFootyHistory : MagicMock')
        #self.mock_open.assert_any_call(
        #        '../Analysis/E0/History.MagicMock.csv', 'w', 
        #        newline='')
        self.mock_Logger().info.assert_any_call('League : E0...')
        #self.mock_open.assert_any_call(
        #        '../Analysis/D1/History.MagicMock.csv', 'w', 
        #        newline='')
        self.mock_Logger().info.assert_any_call('League : D1...')
        self.mock_csv_writer().writerow.assert_any_call(
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
        
        self.mock_csv_writer().writerow.assert_any_call([
                '01/01/2018', 'Chelsea', 'Arsenal', 0, 'H'])
        self.mock_Logger().info.assert_any_call('Writing summary data...')
        #self.mock_open.assert_any_call(
        #        '../Analysis/D1/Summary.MagicMock.csv', 'w', 
        #        newline='')
        #self.mock_open.assert_any_call(
        #        '../Analysis/E0/Summary.MagicMock.csv', 'w', 
        #        newline='')
        self.mock_csv_writer().writerow.assert_any_call([
                'Mark', 'Frequency', '%H','HO', '%D', 'DO', '%A', 'AO'])
        self.mock_csv_writer().writerow.assert_any_call([
                0, 2, '100.00', '1.00', '0.00', '0.00', '0.00', '0.00'])

        self.mock_Logger().info.assert_any_call('0 (2 100.00) ')
        #self.mock_open.assert_any_call(
        #        '../Analysis/D1/Stats.MagicMock.csv', 'w', 
        #        newline='')
        #self.mock_open.assert_any_call(
        #        '../Analysis/E0/Stats.MagicMock.csv', 'w', 
        #        newline='')
        self.mock_csv_writer().writerow.assert_any_call([
                'Result', 'Slope', 'Intercept', 'P', 'R', 'R^2', 'Err'])
        self.mock_stats.linregress.assert_any_call([0], [100.0])
        self.mock_stats.linregress.assert_any_call([0], [0.0])
        self.mock_Logger().info.assert_any_call('Home: 50.00 10.00 0.45 0.50 0.25 0.24')
        self.mock_Logger().info.assert_any_call('Draw: 50.00 10.00 0.45 0.50 0.25 0.24')
        self.mock_Logger().info.assert_any_call('Away: 50.00 10.00 0.45 0.50 0.25 0.24')

        self.mock_csv_writer().writerow.assert_any_call([
                'H', '50.00', '10.00', '0.45', '0.50', '0.25', '0.24'])
        self.mock_csv_writer().writerow.assert_any_call([
                'D', '50.00', '10.00', '0.45', '0.50', '0.25', '0.24'])
        self.mock_csv_writer().writerow.assert_any_call([
                'A', '50.00', '10.00', '0.45', '0.50', '0.25', '0.24'])

if __name__ == '__main__':
    import unittest
    unittest.main()
