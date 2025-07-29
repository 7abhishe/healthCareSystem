import os
from flask import Blueprint, render_template, request, redirect, url_for, flash

upload = Blueprint('upload', __name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload.route('/upload_report', methods=['GET', 'POST'])
def upload_report():
    if request.method == 'POST':
        file = request.files['report']
        patient_name = request.form['patient']
        if file and allowed_file(file.filename):
            folder_path = os.path.join(UPLOAD_FOLDER, patient_name)
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, file.filename)
            file.save(file_path)
            flash("File uploaded successfully!", "success")
            return redirect(url_for('upload.upload_report'))
        else:
            flash("Invalid file type!", "danger")
    return render_template('upload_report.html')