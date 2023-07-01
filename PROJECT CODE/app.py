from flask import Flask,render_template,request
import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static')

MODEL_PATH = 'iceberg.h5'
model = load_model(MODEL_PATH)

def read_image(filename):
    img = image.load_img(filename, target_size=(75, 75))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    if (np.max(img) > 1):
        img = img / 255.0
    return img

@app.route('/')
def index_view():
    return render_template('index.html')

UPLOAD_FOLDER = os.path.join('static', 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        img = read_image(file_path)
        prob = model.predict(img)
        prob = prob[0][0]
        pred = np.array( model.predict(img) > 0.5)
        if (pred):
            output = "ship"
        else:
            output = "iceberg"

        return render_template('index.html', result = output, prob=prob, user_image=file_path)
    else:
        return "Unable to read the file. Please check file extension"

if __name__  == '__main__':
    app.run(debug=True)