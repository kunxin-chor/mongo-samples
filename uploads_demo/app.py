from flask import Flask, render_template, request, redirect, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
import pymongo
import os

app = Flask(__name__)

upload_dir = "/static/uploads/images/"
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
app.config['UPLOADS_DEFAULT_DEST']= TOP_LEVEL_DIR + "/static/uploads/"
app.config['UPLOADED_IMAGES_DEST'] = TOP_LEVEL_DIR + upload_dir
app.config['UPLOADED_IMAGES_URL'] = upload_dir

# create an UploadSet and name it as images
images_upload_set = UploadSet("images", IMAGES)
configure_uploads(app, images_upload_set)

#configure mongo
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'images_db'
conn = pymongo.MongoClient(MONGO_URI)
db = conn[DATABASE_NAME]
#endconfigure

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/', methods=['POST'])
def upload():
    image = request.files.get('image')
    filename = images_upload_set.save(image)
    url = images_upload_set.url(filename)
    db['gallery'].insert_one({
        'image_url': url
    })
    
    return images_upload_set.url(filename)

@app.route('/gallery')
def gallery():
    all_images = db['gallery'].find()
    return render_template('gallery.html', all_images = all_images)

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)