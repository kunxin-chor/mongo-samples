from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import os
import pymongo
from bson.objectid import ObjectId

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
    
    messages = get_flashed_messages()
    print(messages)
    
    # STEP 2 - Fetch all the existing todos --> as a Python dictionary
    results = conn[DATABASE_NAME][TASKS].find({})

    
    # STEP 3 - Return a template and assign the results to a placeholder in the template
    return render_template('index.html', data=results)


# STEP A1 - Route to show the form
@app.route('/task/new')
def create_task():
    return render_template('create_task.html', data={})

#STEP A2 - Create the route to process the form
@app.route('/task/new', methods=['POST'])
def process_create_task():
    #STEP A3 - Extract out the fields
    title = request.form.get('title')
    description = request.form.get('description')
    
    #STEP A4: Insert a new task
    conn[DATABASE_NAME][TASKS].insert({
        'title' : title, # right hand side title is not in quotes, so it's a variable
        'description': description
    })
    #STEP A5 : Add in a flash message
    flash("You have created the new task: " + title)
    
    #STEP A6 : After redirect
    return redirect(url_for('index'))

@app.route('/task/<taskid>/update')
def update_task(taskid):
    
    # STEP B1 - Use the database to find by object id.
    # If we use find_one, we get the result as dictionary
    task = conn[DATABASE_NAME][TASKS].find_one({
        "_id":ObjectId(taskid)
    })
  
    # STEP B2 - Render the template with the existing task information
    return render_template('update_task.html', data=task)
    
#STEP B3 - To process the update form
@app.route('/task/<taskid>/update', methods=['POST'])
def process_update_task(taskid):
    title = request.form.get('title')
    description = request.form.get('description')
    
    # Use mongo to update
    conn[DATABASE_NAME][TASKS].update({
        '_id':ObjectId(taskid)
    }, {
        '$set': {
            'title' : title,
            'description': description
        }
    })
    
    # Set the flash message
    flash("Task updated")
    
    # redirect back to the index route
    return redirect(url_for('index'))

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)