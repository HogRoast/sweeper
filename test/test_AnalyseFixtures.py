# coding: utf-8

import configparser, smtplib
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from Footy.src.AnalyseFixtures import analyseFixtures, fSD, fST, hl, mail_hl

class TestAnalyseFixtures(TestCase):
    """AnalyseFixtures tests"""

    def mock_getFootyConfig(self):
        algoCfg = { 
            'seasons' : ['1718', '1617'],
            'rangeMap' : {
                'E0' : range(-1, 2),
                'D1' : range(0, 4)
            },           
            'season' : '1819',
            'teamErrorMap' : { 
                                'bad team' : 'good team'
                             },
        }
        mailCfg = {
                'fromAddr' : 'an_email@gmail.com',
                'toAddrs' : ['someone@gmail.com', 
                                'someone_else@gmail.com'],
                'pwd' : 'password',
                'svr' : 'server123',
                'port' : 1234
                }
        return (algoCfg, mailCfg)

    def mockGlobals(self):
        self.orig_getFootyConfig = analyseFixtures.__globals__['getFootyConfig']
        self.orig_newCSVFile = analyseFixtures.__globals__['newCSVFile']
        self.orig_readCSVFileAsDict = \
                analyseFixtures.__globals__['readCSVFileAsDict']
        self.orig_Logger = analyseFixtures.__globals__['Logger']
        self.orig_smtplib_SMTP = analyseFixtures.__globals__['smtplib'].SMTP
        self.orig_model = analyseFixtures.__globals__['model']

        analyseFixtures.__globals__['getFootyConfig'] = self.mock_getFootyConfig
        analyseFixtures.__globals__['newCSVFile'] = self.mock_newCSVFile
        analyseFixtures.__globals__['readCSVFileAsDict'] = \
                self.mock_readCSVFileAsDict
        analyseFixtures.__globals__['Logger'] = self.mock_Logger
        analyseFixtures.__globals__['smtplib'].SMTP = self.mock_smtplib_SMTP
        analyseFixtures.__globals__['model'] = self.mock_model

    def resetGlobals(self):
        analyseFixtures.__globals__['getFootyConfig'] = self.orig_getFootyConfig
        analyseFixtures.__globals__['newCSVFile'] = self.orig_newCSVFile
        analyseFixtures.__globals__['readCSVFileAsDict'] = \
                self.orig_readCSVFileAsDict
        analyseFixtures.__globals__['Logger'] = self.orig_Logger
        analyseFixtures.__globals__['smtplib'].SMTP = self.orig_smtplib_SMTP
        analyseFixtures.__globals__['model'] = self.orig_model

    def mock_csvData__iter__(self, other):
        self.csvDataCount += 1
        return self.csvData[self.csvDataCount-1].__iter__()

    def setUp(self):
        self.mock_newCSVFile = MagicMock()
        self.mock_Logger = MagicMock()
        self.csvDataCount = 0
        self.csvData = [[{
                    'b\"Div' : 'E0',
                    'Date' : '27/09/17', 
                    'HomeTeam' : 'Arsenal',
                    'AwayTeam' : 'Chelsea', 
                    'FTR' : 'H'
                    }],[{
                    'Mark' : '0',
                    'Frequency': '200',
                    '%H' : '45.4',
                    'HO' : '2.2',
                    '%D' : '20.3',
                    'DO' : '4.4',
                    '%A' : '34.3',
                    'AO' : '3.3',}]]
        self.mock_readCSVFileAsDict = MagicMock()
        self.mock_readCSVFileAsDict().__enter__().__iter__ = \
                self.mock_csvData__iter__

        self.mock_smtplib_SMTP = MagicMock(spec=smtplib.SMTP)

        self.mock_model = MagicMock(spec=['processMatches', 'markMatch'])
        self.mock_model.processMatches = MagicMock(
                return_value = 'return from mock processMatches')
        self.mock_model.markMatch = MagicMock(return_value = (
                '01/01/18', 'Chelsea', 'Arsenal', 0, 'W:3v0', 'L:2v1'))

        self.mock_stats = MagicMock(spec=['linregress'])
        self.mock_stats.linregress = MagicMock(
                return_value = (50.0, 10.0, 0.5, 0.45, 0.24))

        self.mockGlobals()

    def tearDown(self):
        self.resetGlobals()

    def test_fSD(self):
        self.assertEqual(fSD((1, 2.3, 4.5)),      '(   1   2.30%  4.50)')

    def test_fST(self):
        self.assertEqual(fST(('H#', 'H%', 'HO')), '(H#   H%      HO   )')

    def test_hl(self):
        self.assertEqual(hl('Test'), '\033[1mTest\033[0m')

    def test_mail_hl(self):
        self.assertEqual(
                mail_hl('<td>Test</td>'), '<td bgcolor="yellow">Test</td>')
        self.assertEqual(
                mail_hl('<td align="right">Test</td>'), 
                    '<td align="right" bgcolor="yellow">Test</td>')

    def test_analyseFixtures(self):
        results = 'http://test.com/{}/{}.csv'
        fixtures = 'http://test.com/fixtures.csv'
        opts = ['test', '-s']
        analyseFixtures(results, fixtures, opts)

        self.mock_readCSVFileAsDict.assert_any_call(fixtures)
        self.mock_Logger().debug.assert_any_call(self.csvData[0][0])

        res = results.format('1819', 'E0')
        self.mock_Logger().info.assert_any_call(res)
        self.mock_readCSVFileAsDict.assert_any_call(res)
        self.mock_readCSVFileAsDict.assert_any_call(
                '../Analysis/E0/Summary.MagicMock.csv')
        self.assertTrue(self.mock_model.processMatches.called)

        self.mock_model.markMatch.has_calls(
                'return from mock processMatches', '27/09/17', 
                'Arsenal', 'Chelsea')

        self.mock_newCSVFile().__enter__().writerow.assert_any_call(
                ('E0', '01/01/18', 'Chelsea', 'Arsenal', 0, 90, 45.4, 
                    2.2, 'W:3v0', 'L:2v1'))

        self.mock_Logger().info.assert_any_call('\n\033[1mLge  Date     HomeTeam         AwayTeam         Mark (H#   H%      HO   ) HomeTeamForm                          AwayTeamForm                         \033[0m\n\033[1mE0   01/01/18 Chelsea          Arsenal             0 (  90  45.40%  2.20) (W:3v0) (L:2v1)\033[0m\n')
        
        calls = [call('server123', 1234),
                 call().ehlo(),
                 call().starttls(),
                 call().ehlo(),
                 call().login('an_email@gmail.com', 'password'),
                 call().sendmail('an_email@gmail.com', ['someone@gmail.com', 'someone_else@gmail.com'], \
                     'MIME-Version: 1.0\nContent-type: text/html\nSubject: Footy Bets\n\n<table border=1><tr><th>Lge</th><th>Date</th><th>HomeTeam</th><th>AwayTeam</th><th>Mark</th><th>H#</th><th>H%</th><th>H Odds</th><th>HomeTeamForm</th><th>AwayTeamForm</th></tr><tr><td bgcolor="yellow">E0</td><td bgcolor="yellow">01/01/18</td><td bgcolor="yellow">Chelsea</td><td bgcolor="yellow">Arsenal</td><td align="right" bgcolor="yellow">   0</td><td align="right" bgcolor="yellow">  90</td><td align="right" bgcolor="yellow"> 45.40%</td><td align="right" bgcolor="yellow"> 2.20</td><td align="right" bgcolor="yellow">W:3v0</td><td align="right" bgcolor="yellow">L:2v1</td></tr></table>'),
                 call().quit()]
        self.mock_smtplib_SMTP.assert_has_calls(calls)

        self.mock_Logger().info.assert_any_call("email sent to: ['someone@gmail.com', 'someone_else@gmail.com']")

if __name__ == '__main__':
    import unittest
    unittest.main()
