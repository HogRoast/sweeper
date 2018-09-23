# coding: utf-8

from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, pprint, csv, datetime
import urllib.request
from Logging import Logger
from src.FootyAnalysisTools import strToDate, BaseModel, GoalsScoredSupremacy

class TestFootyAnalysisTools(TestCase):
    """FootyAnalysisTools tests"""

    def setUp(self):
        """
        self.mock_ConfigParser = MagicMock(spec=configparser.ConfigParser)
        self.mock_ConfigParser().__getitem__ = MagicMock(return_value = { 
            'seasons' : "['1718', '1617']",
            'rangeMap' : '''{
                'E0' : range(-1, 2),
                'D1' : range(0, 4)
            }'''
        })
        self.mock_Logger = MagicMock(spec=Logger)
        self.mock_urlopen = MagicMock(spec=urllib.request.urlopen)
        self.csv_data = 'Div_with_control_chars,Date,HomeTeam,AwayTeam\\r\\nB1,29/07/2011,Oud-Heverlee Leuven,Anderlecht'
        self.mock_urlopen().read = MagicMock(return_value = self.csv_data)
        self.csv_data_as_list = self.csv_data.split('\\r\\n')
        i = 0
        for s in self.csv_data_as_list:
            self.csv_data_as_list[i] = s.split(',')
            i += 1
        self.mock_csv_reader = MagicMock(spec=csv.reader, return_value=self.csv_data_as_list)
        self.mock_csv_writer = MagicMock(spec=csv.writer)
        self.mock_open = MagicMock(spec=open, return_value='output file')

        #pprint.pprint(downloadData.__globals__)
        downloadData.__globals__['ConfigParser'] = self.mock_ConfigParser
        downloadData.__globals__['Logger'] = self.mock_Logger
        downloadData.__globals__['urllib'].request.urlopen = self.mock_urlopen
        downloadData.__globals__['csv'].reader = self.mock_csv_reader
        downloadData.__globals__['csv'].writer = self.mock_csv_writer
        downloadData.__globals__['__builtins__']['open'] = self.mock_open
        """

    def test_strToDate(self):
        expected = datetime.date(year=2018, month=1, day=1)
        self.assertEqual(strToDate('01/01/18'), expected)
        self.assertEqual(strToDate('01/01/2018'), expected)
        with self.assertRaises(ValueError) as cm: 
            strToDate('32/01/18')

    def test_BaseModel_processMatches(self):
        ''' processMatches returns result data manipulated by a visitor
            function '''
        results = [{'Date' : '01/01/2018',
                    'HomeTeam' : ' Chelsea',
                    'AwayTeam' : '  Arsenal   ',
                    'FTHG' : '3',
                    'FTAG' : '2',
                    'FTR' : 'H'},
                   {'Date' : '02/02/2018',
                    'HomeTeam' : 'West Ham  ',
                    'AwayTeam' : '  Spurs',
                    'FTHG' : '0',
                    'FTAG' : '0',
                    'FTR' : 'D'},
                   {'Dated' : '03/03/2018',
                    'HomeTeam' : 'Home1',
                    'AwayTeam' : 'Away1',
                    'FTHG' : '0',
                    'FTAG' : '1',
                    'FTR' : 'A'},
                   {'Dated' : '04/04/2018',
                    'HomeTeam' : None,
                    'AwayTeam' : 'Man City',
                    'FTHG' : '3',
                    'FTAG' : '1',
                    'FTR' : 'H'},
                   ]

        def visitor(a, b, c, d, e):
            a[c] = (d, e)
            return a

        model = BaseModel()
        data = model.processMatches(results, visitor)
        self.assertEqual(len(data), 2)
        self.assertEqual(data['01/01/2018'], ('Chelsea', 'Arsenal'))
        self.assertEqual(data['02/02/2018'], ('West Ham', 'Spurs'))

    def test_BaseModel_markMatch(self):
        ''' markMatch returns historical result data condensed into a 
            single marked matched for a given fixture '''
    
        matchData = {'Arsenal' : [('01/01/2018', 2, 'W:2v1'),
                                  ('02/01/2018', 1, 'D:1v1'),
                                  ('03/01/2018', 3, 'W:3v1')],
                     'Chelsea' : [('01/01/2018', 3, 'L:3v4'),
                                  ('02/01/2018', 2, 'D:2v2')],
                    }
        model = BaseModel()
        # working model
        model.markMatch.__globals__['numMatches'] = 2
        r = model.markMatch(matchData, ' 03/01/2018 ', 'Chelsea ', ' Arsenal')
        self.assertEqual(r, ('03/01/2018', 'Chelsea', 'Arsenal', 1, 'L:3v4 D:2v2', 'D:1v1 W:3v1')) 

        # not enough away matches
        model.markMatch.__globals__['numMatches'] = 3
        r = model.markMatch(matchData, ' 03/01/2018 ', 'Chelsea ', ' Arsenal')
        self.assertEqual(r, ('03/01/2018', 'Chelsea', 'Arsenal', None, None, None)) 

        # not enough home or away matches
        model.markMatch.__globals__['numMatches'] = 4
        r = model.markMatch(matchData, ' 03/01/2018 ', 'Chelsea ', ' Arsenal')
        self.assertEqual(r, ('03/01/2018', 'Chelsea', 'Arsenal', None, None, None)) 

        # no match data
        model.markMatch.__globals__['numMatches'] = 2
        r = model.markMatch(None, ' 03/01/2018 ', 'Chelsea ', ' Arsenal')
        self.assertEqual(r, ('03/01/2018', 'Chelsea', 'Arsenal', None, None, None)) 

        # no home team
        model.markMatch.__globals__['numMatches'] = 2
        r = model.markMatch(matchData, ' 03/01/2018 ', None, ' Arsenal')
        self.assertEqual(r, ('03/01/2018', None, 'Arsenal', None, None, None)) 

        # misspelt home team
        model.markMatch.__globals__['numMatches'] = 2
        r = model.markMatch(matchData, ' 03/01/2018 ', 'Chewlsea', ' Arsenal')
        self.assertEqual(r, ('03/01/2018', 'Chewlsea', 'Arsenal', None, None, None)) 

        # no away team
        model.markMatch.__globals__['numMatches'] = 2
        r = model.markMatch(matchData, ' 03/01/2018 ', 'Chelsea', None)
        self.assertEqual(r, ('03/01/2018', 'Chelsea', None, None, None, None)) 

        # misspelt away team
        model.markMatch.__globals__['numMatches'] = 2
        r = model.markMatch(matchData, ' 03/01/2018 ', 'Chelsea', ' Arsenhole')
        self.assertEqual(r, ('03/01/2018', 'Chelsea', 'Arsenhole', None, None, None)) 

        # no match date
        model.markMatch.__globals__['numMatches'] = 2
        r = model.markMatch(matchData, None, 'Chelsea', ' Arsenal')
        self.assertEqual(r, (None, 'Chelsea', 'Arsenal', None, None, None)) 

        # no match date
        model.markMatch.__globals__['numMatches'] = 2
        r = model.markMatch(matchData, '', 'Chelsea ', ' Arsenal')
        self.assertEqual(r, ('', 'Chelsea', 'Arsenal', None, None, None)) 

        # match date is prior to historic data
        model.markMatch.__globals__['numMatches'] = 2
        r = model.markMatch(matchData, '31/12/2017', 'Chelsea ', ' Arsenal')
        self.assertEqual(r, ('31/12/2017', 'Chelsea', 'Arsenal', None, None, None)) 

    def test_GoalsScoredSupremacy_calculateGoalsScored(self):
        row = {'FTHG' : '3', 'FTAG' : '2', 'FTR' : 'H'}
        expected = {'Arsenal' : [('04/01/2018', 3, 'W:3v2')],
                    'Chelsea' : [('04/01/2018', 2, 'L:3v2')],
                   }
        model = BaseModel()

        model = GoalsScoredSupremacy()
        r = model.calculateGoalsScored({}, row, '04/01/2018', 'Arsenal', 'Chelsea')
        self.assertEqual(r, expected) 

if __name__ == '__main__':
    import unittest
    unittest.main()
