# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, sys, csv
from Footy.src.DownloadData import downloadData

class TestDownloadData(TestCase):
    """DownloadData tests"""

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
        self.orig_getFootyConfig = downloadData.__globals__['getFootyConfig']
        self.orig_Logger = downloadData.__globals__['Logger']
        self.orig_newCSVFile = downloadData.__globals__['newCSVFile']
        self.orig_readCSVFileAsDict = \
                downloadData.__globals__['readCSVFileAsDict']

        downloadData.__globals__['getFootyConfig'] = self.mock_getFootyConfig
        downloadData.__globals__['Logger'] = self.mock_Logger
        downloadData.__globals__['newCSVFile'] = self.mock_newCSVFile
        downloadData.__globals__['readCSVFileAsDict'] = \
                self.mock_readCSVFileAsDict

    def resetGlobals(self):
        downloadData.__globals__['getFootyConfig'] = self.orig_getFootyConfig
        downloadData.__globals__['Logger'] = self.orig_Logger
        downloadData.__globals__['newCSVFile'] = self.orig_newCSVFile
        downloadData.__globals__['readCSVFileAsDict'] = \
                self.orig_readCSVFileAsDict

    def mock_csvData__iter__(self, other):
        return self.csv_data.__iter__()

    def mock_csvData__next__(self, other):
        return self.csv_data.__next__()

    def setUp(self):
        self.csv_data = [
                ['Div_with_control_chars','Date','HomeTeam','AwayTeam'],
                ['B1','29/07/2011','Oud-Heverlee Leuven','Anderlecht']]
        self.mock_Logger = MagicMock()
        self.mock_newCSVFile = MagicMock()
        self.mock_readCSVFileAsDict = MagicMock()
        self.mock_readCSVFileAsDict().__enter__().__iter__ = \
                self.mock_csvData__iter__
        self.mock_readCSVFileAsDict().__enter__().__next__ = \
                self.mock_csvData__next__

        self.mockGlobals()

    def tearDown(self):
        self.resetGlobals()

    def test_download(self):
        urlTmpl = 'http://test.com/{}/{}.csv'
        outFile = 'test_{}_{}.out'
        downloadData(urlTmpl, outFile)

        calls = (
                    call('Downloading...'+urlTmpl.format('1718', 'E0')),
                    call('Output to...'+outFile.format('E0', '1718')),
                    call('Downloading...'+urlTmpl.format('1617', 'E0')),
                    call('Output to...'+outFile.format('E0', '1617')),
                    call('Downloading...'+urlTmpl.format('1718', 'D1')),
                    call('Output to...'+outFile.format('D1', '1718')),
                    call('Downloading...'+urlTmpl.format('1617', 'D1')),
                    call('Output to...'+outFile.format('D1', '1617')),
                )
        self.mock_Logger().info.assert_has_calls(calls)

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

if __name__ == '__main__':
    import unittest
    unittest.main()
