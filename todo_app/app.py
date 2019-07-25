from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages, jsonify
import os
import pymongo
import model
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

# STEP 1 - Create a home route and test it
@app.route('/') # map the root route to the index function
def index():
    
    messages = get_flashed_messages()

    # STEP 2 - Fetch all the existing todos --> as a Python dictionary
    results = model.get_all_tasks()

    
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
    model.create_task(title, description, completed)
    
    #STEP A5 : Add in a flash message
    flash("You have created the new task: " + title)
    
    #STEP A6 : After redirect
    return redirect(url_for('index'))

@app.route('/task/<taskid>/update')
def update_task(taskid):
    
    # STEP B1 - Use the database to find by object id.
    # If we use find_one, we get the result as dictionary
    model.find_task(taskid)
  
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
        
    task = model.find_task(taskid)
    
    # Use mongo to update
    model.update_task(taskid, title, description, completed)
    # Set the flash message
    flash("Task updated")
    
    # redirect back to the index route
    return redirect(url_for('index'))
    
@app.route('/task/<taskid>/toggle', methods=['POST'])
def toggle_task(taskid):
    
    task = model.toggle_task(taskid)
    
    flash("Task '{}' has been set to {}".format(task['title'], not task['completed']))
    return redirect(url_for('index'))


#STEP C1 : Add in a route to confirm with the user if he really wants to delete
@app.route('/task/<taskid>/confirm_delete')
def confirm_delete_task(taskid):
    task = model.find_task(taskid)
    return render_template('confirm_delete_task.html', data=task)
    
#STEP C2: Add in a route that actually does the delete
@app.route('/task/<taskid>/delete')
def delete_task(taskid):
    
    task = model.find_task(taskid)
    
    model.delete_task(taskid)
    
    flash("Task: {} has been deleted".format(task['title']))
    return redirect(url_for('index'))
    
@app.route('/client/tasks')
def client_tasks():
    return render_template('client_tasks.html')

# @app.route('/api/v1/todos', methods=['GET'])
# def api_get_tasks():
    
#     tasks = conn[DATABASE_NAME][TASKS].aggregate([
#     {
#         '$project': {
#             'title': 1,
#             'description': { '$ifNull': [ "$description", "No description"] },
#             'completed': { '$ifNull': ['$completed', False] }
#         }
#      }
#     ])

#     results = []
#     for t in tasks:
#         t['_id'] = str(t['_id'])
#         results.append(t)
#     return jsonify(results)
    
    
@app.route('/api/v2/todos', methods=['GET'])
def api_get_tasks_v2():
    tasks = model.get_all_tasks()
    tasks_lists=[]
    for t in tasks:
        t['_id'] = str(t['_id'])
        if 'completed' not in t:
            t['completed'] = False
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
    model.create_task(title, description, completed)
    
    #STEP A6 : After redirect
    return jsonify({
        'message': 'success'
    })
    
@app.route('/api/v1/task/<taskid>/toggle', methods=['PATCH'])
def api_toggle_task(taskid):
    
    task = model.toggle_task(taskid)
    
    return jsonify({
        'message':'success'
    })

@app.route('/api/v1/task/<taskid>', methods=['DELETE'])
def api_delete_task(taskid):
    
    model.delete_task(taskid)
    
    return jsonify({
        'message':'success'
    })


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)