# coding: utf-8

from datetime import datetime
from unittest import TestCase
from sweeper.algos import AlgoFactory

class TestAlgos(TestCase):
    """Algos test stubs"""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_AlgoFactory_create(self):
        algo = AlgoFactory.create('GoalsScoredSupremacy')
        self.assertEqual(algo.__class__.__name__, 'GoalsScoredSupremacy')
        self.assertEqual(algo.numMatches, 6)

if __name__ == '__main__':
    import unittest
    unittest.main()
