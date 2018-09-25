# coding: utf-8

from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, pprint, csv, datetime
import urllib.request
from Logging import Logger
from src.FootyAnalysisTools import strToDate, BaseModel, GoalsScoredSupremacy, MatchResultSupremacy, GoalDifferenceSupremacy

class TestFootyAnalysisTools(TestCase):
    """FootyAnalysisTools tests"""

    def setUp(self):
        pass

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
        ''' Collate match goals scored per team '''

        row = {'FTHG' : '3', 'FTAG' : '2', 'FTR' : 'H'}
        expected1 = {'Arsenal' : [('04/01/2018', 3, 'W:3v2')],
                    'Chelsea' : [('04/01/2018', 2, 'L:3v2')],
                   }
        model = GoalsScoredSupremacy()
        r = model.calculateGoalsScored({}, row, '04/01/2018', 'Arsenal', 'Chelsea')
        self.assertEqual(r, expected1) 

        expected2 = {'Arsenal' : [('04/01/2018', 3, 'W:3v2'),
                                  ('06/01/2018', 0, 'L:6v0')],
                    'Chelsea' : [('04/01/2018', 2, 'L:3v2'),
                                 ('06/01/2018', 6, 'W:6v0')],
                   }

        row2 = {'FTHG' : '6', 'FTAG' : '0', 'FTR' : 'H'}
        r = model.calculateGoalsScored(r, row2, '06/01/2018', 'Chelsea', 'Arsenal')
        self.assertEqual(r, expected2)

    def test_MatchResultSupremacy(self):
        ''' Collate match results per team '''

        row = {'FTR' : 'H'}
        expected1 = {'Arsenal' : [('04/01/2018', 1)],
                     'Chelsea' : [('04/01/2018', 0)],
                   }
        model = MatchResultSupremacy()
        r = model.calculateMatchResult({}, row, '04/01/2018', 'Arsenal', 'Chelsea')
        self.assertEqual(r, expected1) 
        
        row2 = {'FTR' : 'A'}
        
        expected2 = {'Arsenal' : [('04/01/2018', 1),
                                  ('06/01/2018', 0)],
                     'Chelsea' : [('04/01/2018', 0),
                                  ('06/01/2018', 1)],
                    }
        model = MatchResultSupremacy()
        r = model.calculateMatchResult(r, row2, '06/01/2018', 'Arsenal', 'Chelsea')
        self.assertEqual(r, expected2) 
        
    def test_GoalDifferenceSupremacy(self):
        ''' Collate match goal difference per team '''

        row = {'FTHG' : '3', 'FTAG' : '2'}
        expected1 = {'Arsenal' : [('04/01/2018', 1)],
                     'Chelsea' : [('04/01/2018', -1)],
                   }
        model = GoalDifferenceSupremacy()
        r = model.calculateGoalDifference({}, row, '04/01/2018', 'Arsenal', 'Chelsea')
        self.assertEqual(r, expected1) 

        row2 = {'FTHG' : '4', 'FTAG' : '8'}
        expected2 = {'Arsenal' : [('04/01/2018', 1),
                                  ('06/01/2018', -4)],
                     'Chelsea' : [('04/01/2018', -1),
                                  ('06/01/2018', 4)],
                    }
        model = GoalDifferenceSupremacy()
        r = model.calculateGoalDifference(r, row2, '06/01/2018', 'Arsenal', 'Chelsea')
        self.assertEqual(r, expected2) 

if __name__ == '__main__':
    import unittest
    unittest.main()
