# coding: utf-8

import os
from datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, call
from dataclasses import FrozenInstanceError
from Footy.src.database.algo import Algo, AlgoKeys, AlgoValues
from Footy.src.database.database import DatabaseKeys

class TestAlgo(TestCase):
    """Algo object tests"""

    @classmethod
    def setUpClass(cls):
        os.system('cat ../database/create_db.sql | sqlite3 ../database/footy.test.db')
        os.system('cat ../database/*_test_data.sql | sqlite3 ../database/footy.test.db')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_keys_Immutablility(self):
        keys =AlgoKeys(99)

        with self.assertRaises(FrozenInstanceError) as cm:
            keys.id = 75
            
        self.assertIn('cannot assign to field', cm.exception.args[0])

    def test_keys_adhoc(self):
        l = Algo.createAdhoc(DatabaseKeys('algo', None))
        self.assertEqual(l.keys.table, 'algo')
        self.assertTrue(l.keys.fields is None)

    def test_createSingle(self):
        obj = Algo.createSingle((99, 'algo name TD', 'algo desc TD'))

        self.assertEqual(obj.keys.id, 99)
         
        self.assertEqual(obj.vals.name, 'algo name TD')
        self.assertEqual(obj.vals.desc, 'algo desc TD')
         

    def test_createMulti(self):
        rows = [(99, 'algo name TD', 'algo desc TD'),
                (98, 'algo name TD2', 'algo desc TD2')]
        objs = Algo.createMulti(rows)
        
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0].keys.id, 99)
        
        self.assertEqual(objs[0].vals.name, 'algo name TD')
        self.assertEqual(objs[0].vals.desc, 'algo desc TD')
        
        self.assertEqual(objs[1].keys.id, 98)
        
        self.assertEqual(objs[1].vals.name, 'algo name TD2')
        self.assertEqual(objs[1].vals.desc, 'algo desc TD2')
        

    def test_repr(self):
        obj = Algo(99, 'algo name TD', 'algo desc TD')
        self.assertEqual(str(obj), "algo : Keys {'id': 99} : Values {'name': 'algo name TD', 'desc': 'algo desc TD'}")

if __name__ == '__main__':
    import unittest
    unittest.main()
