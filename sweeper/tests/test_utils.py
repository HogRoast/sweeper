# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from collections import OrderedDict
import configparser, pprint, csv, sys
import urllib.request
from sweeper.utils import getSweeperOptions, SweeperArgsError, \
        getSweeperConfig, newCSVFile, readCSVFileAsDict, SweeperOptions

class TestUtils(TestCase):
    """tils tests"""

    def test_SweeperOptions(self):
        opts = SweeperOptions()

        opts._set(SweeperOptions.DEBUG_LOGGING)
        self.assertTrue(opts.test(SweeperOptions.DEBUG_LOGGING))

        opts._set(SweeperOptions.CURRENT_SEASON_ONLY)
        self.assertTrue(opts.test(SweeperOptions.CURRENT_SEASON_ONLY))

        opts._set(0b00001000)
        self.assertFalse(opts.test(0b00001000))

    def test_getSweeperOptions(self):
        logger = MagicMock()

        opts = ['test', '-d']
        sopts = getSweeperOptions(logger, opts)
        logger.toggleMask.assert_any_call(0b0001011)
        self.assertTrue(sopts.test(SweeperOptions.DEBUG_LOGGING))

        opts = ['test', '-c']
        sopts = getSweeperOptions(logger, opts)
        self.assertTrue(sopts.test(SweeperOptions.CURRENT_SEASON_ONLY))

        opts = ['test', '-h']
        exitFn = sys.exit
        exitCalled = False
        def mockExit(statusCode): 
            nonlocal exitCalled 
            exitCalled = True
        sys.exit = mockExit
        sopts = getSweeperOptions(logger, opts)
        self.assertTrue(exitCalled)
        sys.exit = exitFn

    def test_getSweeperConfig(self):
        mock_ConfigParser = MagicMock(spec=configparser.ConfigParser)
        d = {
                'base.cfg' : { 'dbName' : '../../config/footy.db' }
            }
        def mock_CP_get(section, option): 
            return d[section][option]
        def mock_CP_options(section):
            return d[section].keys()

        mock_ConfigParser().get = mock_CP_get 
        mock_ConfigParser().options = mock_CP_options 

        orig_ConfigParser = getSweeperConfig.__globals__['ConfigParser']
        getSweeperConfig.__globals__['ConfigParser'] = mock_ConfigParser
        
        baseCfg = getSweeperConfig()
        self.assertEqual(baseCfg['dbName'], '../../config/footy.db')

        # replace the globals that we have been fiddling with
        # MUST be the last line in this test
        getSweeperConfig.__globals__['ConfigParser'] = orig_ConfigParser

    def test_createAndReadCSVDict(self):
        fileName = './sweeper/tests/swprtstfile'
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
