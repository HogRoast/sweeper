# coding: utf-8

from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
import configparser, sys, pprint, csv
import urllib.request
from Logging import Logger
from src.DownloadData import downloadData

class TestDownloadData(TestCase):
    """DownloadData tests"""

    def setUp(self):
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
        print(self.csv_data_as_list)
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

    def test_download(self):
        urlTmpl = 'http://test.com/{}/{}.csv'
        outFile = 'test_{}_{}.out'
        downloadData(urlTmpl, outFile)

        self.mock_ConfigParser().read.assert_called_once_with('../config/footy.ini')
        self.mock_ConfigParser().__getitem__.assert_called_once_with('algo.cfg')

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

        calls = (
                    call(outFile.format('E0', '1718'), 'w'),
                    call(outFile.format('E0', '1617'), 'w'),
                    call(outFile.format('D1', '1718'), 'w'),
                    call(outFile.format('D1', '1617'), 'w'),
                )
        self.mock_open.assert_has_calls(calls)

        args = (
                   'output file',
                   'output file',
                   'output file',
                   'output file',
               )
        for a in args:
            self.mock_csv_writer.assert_any_call(a)

        line1 = self.csv_data_as_list[0]
        line1[0] = 'Div'
        line2 = self.csv_data_as_list[1]
        calls = (
                    call(line1),
                    call(line2),
                    call(line1),
                    call(line2),
                    call(line1),
                    call(line2),
                    call(line1),
                    call(line2),
                )
        self.mock_csv_writer().writerow.assert_has_calls(calls)

if __name__ == '__main__':
    import unittest
    unittest.main()
