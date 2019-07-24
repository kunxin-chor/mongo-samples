from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

# STEP 1 - Create a home route and test it
@app.route('/') # map the root route to the index function
def index():
    
    # STEP 2 - Blank, no logic
    
    # STEP 3 - Return a template
    return render_template('index.html')


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)