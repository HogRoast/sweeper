# coding: utf-8

from datetime import datetime
from unittest import TestCase
from src.DownloadData import main

class TestDownloadData(TestCase):
    """DownloadData tests"""

    def setUp(self):
        self.mockLog = []

    def log(self, s):
        self.mockLog.append(s)

if __name__ == '__main__':
    import unittest
    unittest.main()
