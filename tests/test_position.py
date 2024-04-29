

import unittest
import pandas as pd
import numpy as np
import os
import pickle
from config import PICKLE_DATA
from src.dataset import TsData
from src.utils.utils import unix2dt
from src.position import Position

class TestPosition(unittest.TestCase):
    """
    A Unittest class to test the Position class.
    """
    def setUp(self):
        self.data = TsData(pickle_file=PICKLE_DATA)
        self.position = Position()
    
    def test_init(self):
        self.assertIsNone(self.position.entry_date)
        self.assertIsNone(self.position.entry_price)
        self.assertIsNone(self.position.exit_date)
        self.assertIsNone(self.position.exit_price)
        self.assertIsNone(self.position.quantity)
        self.assertIsNone(self.position.entry_cash)
        self.assertIsNone(self.position.exit_cash)
        self.assertIsNone(self.position.returns)
    
    def test_active(self):
        self.assertFalse(self.position.active())
        self.position.entry_date = 1
        self.assertTrue(self.position.active())
        self.position.exit_date = 2
        self.assertFalse(self.position.active())
    
    def test_check_active(self):
        self.position.exit_date = 2
        with self.assertRaises(ValueError):
            self.position.buy(3, 1000, 1000, 0.03)
            
    def test_closed(self):
        self.assertFalse(self.position.closed())
        self.position.exit_date = 2
        self.assertTrue(self.position.closed())
                
    def test_buy(self):
        self.position.buy(2, 1000, 1000, 0.03)
        self.assertEqual(self.position.entry_date, 2)
        self.assertEqual(self.position.entry_price, 1000)
        self.assertEqual(self.position.entry_cash, 1000)
        self.assertEqual(self.position.quantity, 0.970873786407767)
        
    def test_sell(self):
        self.position.buy(2, 1000, 1000, 0.03)
        self.position.sell(3, 1000, 0.03)
        self.assertEqual(self.position.exit_date, 3)
        self.assertEqual(self.position.exit_price, 1000)
        self.assertEqual(self.position.exit_cash, 941.747572815534)
        self.assertEqual(self.position.returns, -58.252427184466)
        
    def test_returns(self):
        self.position.buy(2, 1000, 1000, 0.03)
        self.position.sell(3, 1000, 0.03)
        self.assertEqual(self.position.returns, -58.252427184466)

    def tearDown(self) -> None:
        return super().tearDown()
        
        
def main():
    unittest.main()
    
if __name__ == '__main__':
    main()