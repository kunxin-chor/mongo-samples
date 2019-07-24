from flask import Flask, render_template, request, redirect
import os
import pymongo

app = Flask(__name__)

# STEP 0 - Create the connection to mongo
# 0.1. Retrieve the environment variables
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'todos'
TASKS = 'tasks'

# 0.2. Create the connection
conn = pymongo.MongoClient(MONGO_URI)

# STEP 1 - Create a home route and test it
@app.route('/') # map the root route to the index function
def index():
    
    # STEP 2 - Fetch all the existing todos --> as a Python dictionary
    results = conn[DATABASE_NAME][TASKS].find({})
    
    
    # STEP 3 - Return a template and assign the results to a placeholder in the template
    return render_template('index.html', data=results)


# STEP A1 - Route to show the form
@app.route('/task/new')
def create_task():
    return render_template('create_task.html')

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)