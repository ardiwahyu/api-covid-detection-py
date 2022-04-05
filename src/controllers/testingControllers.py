from flask import request, flash, redirect
import os

ALLOWED_EXTENSIONS = ['wav']
UPLOAD_FOLDER = '../uploads'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_FOLDER), file.filename)
        return 'Success'