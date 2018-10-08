# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, pprint, csv
import urllib.request
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
        self.orig_urlopen = footyBackTest.__globals__['urllib'].request.urlopen
        self.orig_csv_reader = footyBackTest.__globals__['csv'].DictReader
        self.orig_newCSVFile = footyBackTest.__globals__['newCSVFile']
        #self.orig_open = footyBackTest.__globals__['__builtins__']['open']

        footyBackTest.__globals__['getFootyConfig'] = self.mock_getFootyConfig
        footyBackTest.__globals__['Logger'] = self.mock_Logger
        footyBackTest.__globals__['urllib'].request.urlopen = self.mock_urlopen
        footyBackTest.__globals__['csv'].DictReader = self.mock_csv_reader
        footyBackTest.__globals__['newCSVFile'] = self.mock_newCSVFile
        #footyBackTest.__globals__['__builtins__']['open'] = self.mock_open

    def resetGlobals(self):
        footyBackTest.__globals__['getFootyConfig'] = self.orig_getFootyConfig
        footyBackTest.__globals__['Logger'] = self.orig_Logger
        footyBackTest.__globals__['urllib'].request.urlopen = self.orig_urlopen
        footyBackTest.__globals__['csv'].DictReader = self.orig_csv_reader
        footyBackTest.__globals__['newCSVFile'] = self.orig_newCSVFile
        #footyBackTest.__globals__['__builtins__']['open'] = self.orig_open


    def setUp(self):
        self.mock_Logger = MagicMock()
        self.mock_urlopen = MagicMock(spec=urllib.request.urlopen)
        self.csv_summary_data = '''Mark,Frequency,%H,HO,%D,DO,%A,AO
1,273,49.08,2.04,24.18,4.14,26.74,3.74'''
        self.csv_summary_data_as_dict_list = [
                dict(zip(self.csv_summary_data.split('\n')[0].split(','), 
                    self.csv_summary_data.split('\n')[1].split(',')))]
        #self.mock_open = MagicMock(
        #        spec=open, return_value = self.csv_summary_data)
        self.mock_csv_reader = MagicMock(
                spec=csv.DictReader, 
                return_value = self.csv_summary_data_as_dict_list)
        self.mock_newCSVFile = MagicMock()

        self.csv_result_data = 'Div_with_control_chars,Date,HomeTeam,AwayTeam\\r\\nB1,29/07/2011,Oud-Heverlee Leuven,Anderlecht'
        self.mock_urlopen().read = MagicMock(
                return_value = self.csv_result_data)
        self.csv_result_data_as_list = self.csv_result_data.split('\\r\\n')
        i = 0
        for s in self.csv_result_data_as_list:
            self.csv_result_data_as_list[i] = s.split(',')
            i += 1

        self.mockGlobals()

    def tearDown(self):
        self.resetGlobals()

    def test_backtest(self):
        # TEMPORARY!!
        return

        urlTmpl = 'http://test.com/{}/{}.csv'
        footyBackTest(urlTmpl, [])

        #self.mock_open.assert_any_call(
        #        '../Analysis/E0/Summary.GoalsScoredSupremacy.csv', 'r', 
        #        newline='')
        #self.mock_open.assert_any_call(
        #        '../Analysis/D1/Summary.GoalsScoredSupremacy.csv', 'r', 
        #        newline='')
        self.mock_csv_reader.assert_any_call(
                self.csv_summary_data, delimiter=',')
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/E0/BackTest.GoalsScoredSupremacy.csv',
                ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result', 'MyBet', 
                    'MyOdds', 'Bookie', 'BookieOdds', 'Winnings', 'PnL', 
                    'T_Stk', 'T_W', 'Yield'])
        self.mock_newCSVFile.assert_any_call(
                '../Analysis/D1/BackTest.GoalsScoredSupremacy.csv',
                ['Date', 'HomeTeam', 'AwayTeam', 'Mark', 'Result', 'MyBet', 
                    'MyOdds', 'Bookie', 'BookieOdds', 'Winnings', 'PnL', 
                    'T_Stk', 'T_W', 'Yield'])
        self.mock_newCSVFile.writerow.assert_any_call(self.csv_summary_data)

        self.mock_urlopen.assert_any_call('http://test.com/1718/E0.csv') 
        self.mock_urlopen.assert_any_call('http://test.com/1617/E0.csv') 
        self.mock_urlopen.assert_any_call('http://test.com/1718/D1.csv') 
        self.mock_urlopen.assert_any_call('http://test.com/1617/D1.csv') 

if __name__ == '__main__':
    import unittest
    unittest.main()
