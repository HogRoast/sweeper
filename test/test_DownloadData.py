# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, sys, csv
import urllib.request
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
        self.orig_urlopen = downloadData.__globals__['urllib'].request.urlopen
        self.orig_csv_reader = downloadData.__globals__['csv'].reader
        self.orig_newCSVFile = downloadData.__globals__['newCSVFile']

        downloadData.__globals__['getFootyConfig'] = self.mock_getFootyConfig
        downloadData.__globals__['Logger'] = self.mock_Logger
        downloadData.__globals__['urllib'].request.urlopen = self.mock_urlopen
        downloadData.__globals__['csv'].reader = self.mock_csv_reader
        downloadData.__globals__['newCSVFile'] = self.mock_newCSVFile

    def resetGlobals(self):
        downloadData.__globals__['getFootyConfig'] = self.orig_getFootyConfig
        downloadData.__globals__['Logger'] = self.orig_Logger
        downloadData.__globals__['urllib'].request.urlopen = self.orig_urlopen
        downloadData.__globals__['csv'].reader = self.orig_csv_reader
        downloadData.__globals__['newCSVFile'] = self.orig_newCSVFile

    def setUp(self):
        self.mock_Logger = MagicMock()
        self.mock_urlopen = MagicMock(spec=urllib.request.urlopen)
        self.csv_data = 'Div_with_control_chars,Date,HomeTeam,AwayTeam\\r\\nB1,29/07/2011,Oud-Heverlee Leuven,Anderlecht'
        self.mock_urlopen().read = MagicMock(return_value = self.csv_data)
        self.csv_data_as_list = self.csv_data.split('\\r\\n')
        i = 0
        for s in self.csv_data_as_list:
            self.csv_data_as_list[i] = s.split(',')
            i += 1
        
        self.mock_csv_reader = MagicMock(spec=csv.reader, return_value=self.csv_data_as_list)
        self.mock_newCSVFile = MagicMock()

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
            self.mock_urlopen.assert_any_call(a)

        self.mock_csv_reader.assert_any_call(self.csv_data.split('\\r\\n'), delimiter=',')

        line1 = self.csv_data_as_list[0]
        line1[0] = 'Div'
        line2 = self.csv_data_as_list[1]
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
