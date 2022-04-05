from flask import request, flash, redirect
import os
from flask import Flask
from flask_restful import Api
import src.helpers.payload as pl
import src.controllers.detection.testing as testing

app = Flask(__name__)
api = Api(app)

ALLOWED_EXTENSIONS = ['wav']
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/testing', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        res = pl.error_message
        res['code'] = pl.status['error']
        res['message'] = 'No selected file'
        return res
    file = request.files['file']

    if file.filename == '':
        res = pl.error_message
        res['code'] = pl.status['error']
        res['message'] = 'No selected file'
        return res
    if file and allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER, 'cough_file.wav'))
        status, peluang = testing.detect(os.path.join(UPLOAD_FOLDER, 'cough_file.wav'))
        res = pl.success_message
        res['code'] = pl.status['success']
        res['status'] = status
        res['peluang'] = str(peluang)
        return res

if __name__ == '__main__':
    app.run()