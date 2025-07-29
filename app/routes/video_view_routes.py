import os
from flask import Blueprint, render_template

video_view = Blueprint('video_view', __name__)
VIDEO_FOLDER = 'static/videos'

@video_view.route('/view_videos')
def view_videos():
    videos = []
    if os.path.exists(VIDEO_FOLDER):
        for filename in os.listdir(VIDEO_FOLDER):
            if filename.endswith('.webm'):
                videos.append(f'/static/videos/{filename}')
    return render_template('view_videos.html', videos=videos)