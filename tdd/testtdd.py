import unittest
import pymongo
import products
import os


MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'test'
PRODUCTS = 'products'

class SimpleTest(unittest.TestCase):
    def setUp(self):
        self.conn = pymongo.MongoClient(MONGO_URI)
        self.db = self.conn[DATABASE_NAME]
    
    def tearDown(self):
        self.conn.drop_database(DATABASE_NAME)
        self.conn.close()
        
    def test_can_create_product(self):
        products.collection = self.conn[DATABASE_NAME][PRODUCTS]
        products.create_product("Handbag", 33.33, "Made of fake leather", 3)
        
        found_product = self.conn[DATABASE_NAME][PRODUCTS].find_one({'name':'Handbag'})
        self.assertFalse(found_product is None)
        self.assertEqual('Handbag', found_product['name'])
        self.assertEqual(33.33, found_product['price'])
        
        products.create_product("Boardgame", 45.45, "RISK", 10)
        found_product = self.conn[DATABASE_NAME][PRODUCTS].find_one({'name':'Boardgame'})
        self.assertFalse(found_product is None)
    
    def test_can_update_product(self):
        products.collection = self.conn[DATABASE_NAME][PRODUCTS]
        new_product_id = products.create_product("Handbag", 33.33, "Made of fake leather", 3)
        self.assertFalse(new_product_id is None)
        
        products.update_product(new_product_id, "Wallet", 34.34, "Made of real leather", 4)
        
        found_product = self.conn[DATABASE_NAME][PRODUCTS].find_one({'name':'Wallet'})
        self.assertEqual('Wallet', found_product['name'])
        self.assertEqual(34.34, found_product['price'])
        self.assertEqual('Made of real leather', found_product['description'])
        self.assertEqual(4, found_product['quantity'])
        
    
    def test_update_products_can_handle_negative_price(self):
        products.collection = self.conn[DATABASE_NAME][PRODUCTS]
        new_product_id = products.create_product("Handbag", -33.33, "Made of fake leather", 3)
        self.assertTrue(new_product_id is None)
        
        new_product_id = products.create_product("Handbag", 1, "Made of fake leather", -3)
        self.assertTrue(new_product_id is None)

        new_product_id = products.create_product("Handbag", -1, "Made of fake leather", -3)
        self.assertTrue(new_product_id is None)
        
if __name__ == '__main__':
    unittest.main()