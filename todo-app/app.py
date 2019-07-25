from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, jsonify
import os
import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps

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
    completed = request.form.get('completed')
    # because what get through the form is a string
    if completed == 'true':
        completed = True
    else:
        completed = False
    
    
    #STEP A4: Insert a new task
    conn[DATABASE_NAME][TASKS].insert({
        'title' : title, # right hand side title is not in quotes, so it's a variable
        'description': description,
        'completed':completed
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
    completed = request.form.get('completed')
    # because what get through the form is a string
    if completed == 'true':
        completed = True
    else:
        completed = False
        
    task = conn[DATABASE_NAME][TASKS].find_one({
        '_id':ObjectId(taskid)
    })
    
    # Use mongo to update
    conn[DATABASE_NAME][TASKS].update({
        '_id':ObjectId(taskid)
    }, {
        '$set': {
            'title' : title,
            'description': description,
            'completed': completed
        }
    })
    
    # Set the flash message
    flash("Task updated")
    
    # redirect back to the index route
    return redirect(url_for('index'))
    
@app.route('/task/<taskid>/toggle', methods=['POST'])
def toggle_task(taskid):
    
    task = conn[DATABASE_NAME][TASKS].find_one({
        "_id":ObjectId(taskid)
    })
    
    conn[DATABASE_NAME][TASKS].update({
        '_id':ObjectId(taskid)
    }, {
        '$set': {
            'completed': not task['completed']
        }
    })
    
    flash("Task '{}' has been set to {}".format(task['title'], not task['completed']))
    return redirect(url_for('index'))


#STEP C1 : Add in a route to confirm with the user if he really wants to delete
@app.route('/task/<taskid>/confirm_delete')
def confirm_delete_task(taskid):
    task = conn[DATABASE_NAME][TASKS].find_one({
        '_id':ObjectId(taskid)
    })
    return render_template('confirm_delete_task.html', data=task)
    
#STEP C2: Add in a route that actually does the delete
@app.route('/task/<taskid>/delete')
def delete_task(taskid):
    
    task = conn[DATABASE_NAME][TASKS].find_one({
        '_id':ObjectId(taskid)
    })
    
    conn[DATABASE_NAME][TASKS].delete_one({
        '_id':ObjectId(taskid)
    })
    
    flash("Task: {} has been deleted".format(task['title']))
    return redirect(url_for('index'))
    
@app.route('/client/tasks')
def client_tasks():
    return render_template('client_tasks.html')

@app.route('/api/v1/todos', methods=['GET'])
def api_get_tasks():
    
    tasks = conn[DATABASE_NAME][TASKS].aggregate([
    {
        '$project': {
            'title': 1,
            'description': { '$ifNull': [ "$description", "No description"] },
            'completed': { '$ifNull': ['$completed', False] }
        }
     }
    ])

    results = []
    for t in tasks:
        t['_id'] = str(t['_id'])
        results.append(t)
    return jsonify(results)
    
    
@app.route('/api/v2/todos', methods=['GET'])
def api_get_tasks_v2():
    tasks = conn[DATABASE_NAME][TASKS].find()
    tasks_lists=[]
    for t in tasks:
        t['_id'] = str(t['_id'])
        tasks_lists.append(t)
        
        
    return jsonify(tasks_lists)

@app.route('/api/v1/todos', methods=['POST'])
def api_process_create_task():
    #STEP A3 - Extract out the fields
    title = request.json.get('title')
    description = request.json.get('description')
    completed = request.json.get('completed')
    # because what get through the form is a string
    if completed == 'true':
        completed = True
    else:
        completed = False
    
    
    #STEP A4: Insert a new task
    conn[DATABASE_NAME][TASKS].insert({
        'title' : title, # right hand side title is not in quotes, so it's a variable
        'description': description,
        'completed':completed
    })
  
    
    #STEP A6 : After redirect
    return jsonify({
        'message': 'success'
    })
    

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)