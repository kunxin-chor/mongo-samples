import unittest
import pymongo
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
        
    def testCanInsertProducts(self):
        result = self.db[PRODUCTS].insert_one({
            'title' : 'RISK Board Game',
            'sku' : '12345A',
            'user': {
                'username':'paulc',
                'email':'a@a.com'
            }
        })
        
        #locate the product
        product = self.db[PRODUCTS].find_one({
            '_id' : result.inserted_id
        })
        
        self.assertEqual('RISK Board Game', product['title'])
        
if __name__ == '__main__':
    unittest.main()