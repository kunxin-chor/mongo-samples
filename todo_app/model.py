import os
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps

# STEP 0 - Create the connection to mongo
# 0.1. Retrieve the environment variables
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'todos'
TASKS = 'tasks'

# 0.2. Create the connection
conn = pymongo.MongoClient(MONGO_URI)

def get_all_tasks():
    results = conn[DATABASE_NAME][TASKS].find({})
    return results

def find_task(taskid):
    task = conn[DATABASE_NAME][TASKS].find_one({
        "_id":ObjectId(taskid)
    })
    return task

def create_task(title, description, completed):
    result = conn[DATABASE_NAME][TASKS].insert_one({
        'title' : title, # right hand side title is not in quotes, so it's a variable
        'description': description,
        'completed':completed
    })
    return result.inserted_id
    
def delete_task(taskid):
        conn[DATABASE_NAME][TASKS].delete_one({
        '_id':ObjectId(taskid)
    })
    
def update_task(taskid, title, description, completed):
     conn[DATABASE_NAME][TASKS].update({
        '_id':ObjectId(taskid)
    }, {
        '$set': {
            'title' : title,
            'description': description,
            'completed': completed
        }
    })
    

def toggle_task(taskid):
    task = conn[DATABASE_NAME][TASKS].find_one({
        "_id":ObjectId(taskid)
    })
    
    conn[DATABASE_NAME][TASKS].update_one({
        '_id':ObjectId(taskid)
    }, {
        '$set': {
            'completed': not task['completed']
        }
    })
    
    return task