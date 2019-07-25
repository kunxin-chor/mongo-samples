# File name must begin with a 'test'

import unittest
import pymongo
import os
import model

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'test'
TASKS = 'tasks'

# SimpleTest inherits from unittest.Testcase
class ModelTest(unittest.TestCase):
  
    def __init__(self, *args, **kwargs):
        super(ModelTest, self).__init__(*args, **kwargs)
        self.conn = pymongo.MongoClient(MONGO_URI)
        
        
    def setUp(self):
        self.db = self.conn[DATABASE_NAME]
        # replace the database connection in model with the test connection
        model.DATABASE_NAME = DATABASE_NAME
        
    def tearDown(self):
        self.conn[DATABASE_NAME][TASKS].delete_many({})

    def testSanity(self):
        self.assertTrue(True)
        
    def insert_dummy(self):
        self.conn[DATABASE_NAME][TASKS].insert_many([
            {
                'title':'A', 'description':'B', 'completed':False
            },
            {
                'title':'A1', 'description':'B1', 'completed':False
            },
            {
                'title':'A2', 'description':'B2', 'completed':False
            }
                
        ])
        
        
    def test_can_get_tasks(self):
        
        self.insert_dummy()
        tasks = model.get_all_tasks()
        self.assertEqual(3, tasks.count())
        
    def test_can_insert_task(self):
        self.insert_dummy()
        created_task_id = model.create_task("Visit doctor", "ABCABC", True)
        
        tasks = model.get_all_tasks()
        self.assertEqual(4, tasks.count())
        
        task_from_db = model.find_task(created_task_id)
        self.assertEqual('Visit doctor', task_from_db['title'])
        self.assertEqual('ABCABC', task_from_db['description'])
        self.assertEqual(True, task_from_db['completed'])
        
        
    def test_can_toggle_task(self):
        created_task_id = model.create_task("Visit doctor", "ABCABC", True)
        model.toggle_task(created_task_id)
        task_from_db = model.find_task(created_task_id)
        self.assertEqual(False, task_from_db['completed'])
  
  
if __name__ == '__main__':
    unittest.main()