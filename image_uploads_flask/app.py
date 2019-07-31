from flask import Flask, render_template, request
from flask_uploads import UploadSet, IMAGES, configure_uploads
import pymongo
import os

app = Flask(__name__)

#configure uploads
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
upload_dir = '/uploads/img'
app.config["UPLOADS_DEFAULT_DEST"] = TOP_LEVEL_DIR + upload_dir
app.config["UPLOADED_IMAGES_DEST"] = TOP_LEVEL_DIR + upload_dir

images_upload_set = UploadSet('images', IMAGES)
configure_uploads(app, images_upload_set)
#end configure uploads

#configure mongo
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'uploads_demo'
conn = pymongo.MongoClient(MONGO_URI)
db = conn[DATABASE_NAME]
#endconfigure

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/upload', methods=['POST'])
def upload():
    image = request.files.get('image')
    filename = images_upload_set.save(image)
    
    # create the mongo record below
    db["images"].insert_one({
        'image_url' : upload_dir + '/' + filename
    })
    return filename
    
@app.route('/gallery')
def gallery():
    all_images = db['images'].find({});
    return render_template('gallery.html', all_images=all_images,
        images_upload_set=images_upload_set)
    

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)