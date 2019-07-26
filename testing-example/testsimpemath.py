# File name must begin with a 'test'

import unittest
import pymongo
import os
import simplemath

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'test'
PRODUCTS = 'products'

# SimpleTest inherits from unittest.Testcase
class SimpleTest(unittest.TestCase):
  
    def testAddTwoNumbers(self):
        x = simplemath.add_two(2, 3)
        self.assertEqual(5, x)
        
        x = simplemath.add_two(-2, -3)
        self.assertEqual(-5, x)
        
    def testCanCalculateGST(self):
        gst_percent = 0.07
        gst = simplemath.calculate_gst(10, gst_percent)
        self.assertAlmostEqual(10*gst_percent, gst)
        
        gst = simplemath.calculate_gst(10.10, gst_percent)
        self.assertAlmostEqual(round(10.10*gst_percent, 2), gst)
        self.assertNotAlmostEqual(10.10*gst_percent, gst)
        
        gst = simplemath.calculate_gst(-2, gst_percent)
        self.assertEqual(0, gst)
        
if __name__ == '__main__':
    unittest.main()