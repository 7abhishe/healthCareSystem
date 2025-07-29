from flask import Blueprint, render_template, request, session, redirect, url_for
import os
from datetime import datetime

UPLOAD_FOLDER = os.path.join("static", "videos")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

record = Blueprint('record', __name__)


@record.route('/record')
def record_page():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('record.html', user=session['user'])

@record.route('/save_video', methods=['POST'])
def save_video():
    if 'user' not in session:
        return "Unauthorized", 403

    video = request.files['video']
    patient = request.form.get('patient', 'unknown')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{patient}_{timestamp}.webm"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    video.save(filepath)
    return "Video uploaded successfully!"