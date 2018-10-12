# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from collections import OrderedDict
import configparser, pprint, csv
import urllib.request
from Footy.src.FootyUtils import getFootyOptions, FootyArgsError, getFootyConfig, newCSVFile, readCSVFileAsDict

class TestFootyUtils(TestCase):
    """FootyUtils tests"""

    def test_getFootyOptions(self):
        logger = MagicMock()

        opts = ['test']
        (sendMail, rangeMap) = getFootyOptions(logger, opts)
        self.assertFalse(sendMail)
        self.assertEqual(rangeMap, None)

        opts = ['test', '-d']
        (sendMail, rangeMap) = getFootyOptions(logger, opts)
        logger.toggleMask.assert_any_call(0x0001011)

        opts = ['test', '-s']
        (sendMail, rangeMap) = getFootyOptions(logger, opts)
        self.assertTrue(sendMail)

        opts = ['test', '-r']
        with self.assertRaises(FootyArgsError) as cm:
            (sendMail, rangeMap) = getFootyOptions(logger, opts)
        self.assertEqual(cm.exception.msg, '-r option must be followed by dictionary type representing a rangeMap')

        opts = ['test', '-r', '{"faultyKey : "testValue"}']
        with self.assertRaises(FootyArgsError) as cm:
            (sendMail, rangeMap) = getFootyOptions(logger, opts)
        self.assertEqual(cm.exception.msg, 'Failed to evaluate rangeMap arg - {"faultyKey : "testValue"}')

        opts = ['test', '-r', '{"testKey" : "testValue"}']
        opts = ['test', '-r', '{"testKey" : "testValue"}']
        (sendMail, rangeMap) = getFootyOptions(logger, opts)
        self.assertEqual(rangeMap['testKey'], 'testValue')
        self.assertEqual(len(rangeMap.keys()), 1)

    def test_getFootyConfig(self):
        mock_ConfigParser = MagicMock(spec=configparser.ConfigParser)
        d = {
                'algo.cfg' : { 'seasons' : "['1718', '1617']",
                       'rangeMap' : '''{
                                        'E0' : range(-1, 2),
                                        'D1' : range(0, 4)
                                       }''',
                       'teamErrorMap' : '''{
                                            'bad team' : 'good team'
                                           }''',
                      },
                'mail.cfg' : { 'fromAddr' : 'my@email.com',
                       'toAddrs' : '''["your@email.com",
                                       "someones@email.com"
                                      ]''',
                       'pwd' : 'password',
                       'svr' : 'some_server',
                       'port' : '8080'
                     }
            }
        def mock_CP_get(section, option): 
            return d[section][option]
        def mock_CP_options(section):
            return d[section].keys()

        mock_ConfigParser().get = mock_CP_get 
        mock_ConfigParser().options = mock_CP_options 

        orig_ConfigParser = getFootyConfig.__globals__['ConfigParser']
        getFootyConfig.__globals__['ConfigParser'] = mock_ConfigParser
        
        (algoCfg, mailCfg) = getFootyConfig()
        self.assertTrue(len(algoCfg['rangeMap']), 2)
        self.assertEqual(algoCfg['seasons'][0], '1718')
        self.assertTrue(len(algoCfg['seasons']), 2)
        self.assertTrue(len(algoCfg['teamErrorMap']), 1)
        self.assertEqual(algoCfg['teamErrorMap']['bad team'], 'good team')
        self.assertTrue(len(mailCfg['toAddrs']), 2)
        self.assertEqual(mailCfg['pwd'], 'password')

        # replace the globals that we have been fiddling with
        # MUST be the last line in this test
        getFootyConfig.__globals__['ConfigParser'] = orig_ConfigParser

    def test_createAndReadCSVDict(self):
        fileName = '../Data/test_file'
        fieldNames = ['h1', 'h2', 'h3']
        testData = [[1, 2, 3], ['a', 'b', 'c'], [1.2, 1.3, 4.2]]

        with newCSVFile(fileName, fieldNames) as writer:
            for d in testData:
                writer.writerow(d)
        self.assertTrue(writer._fileHandle.closed)

        with readCSVFileAsDict(fileName) as reader:
            j = 0
            for r in reader:
                for i in range(0, 3):
                    self.assertEqual(r[fieldNames[i]], str(testData[j][i]))
                j = j + 1
        self.assertTrue(reader._fileHandle.closed)

    def test_ReadCSVFileAsDict_WithURL(self):
        fileName = 'http://www.football-data.co.uk/fixtures.csv'
        with readCSVFileAsDict(fileName) as reader:
            for r in reader:
                self.assertTrue(isinstance(r, OrderedDict))


if __name__ == '__main__':
    import unittest
    unittest.main()
