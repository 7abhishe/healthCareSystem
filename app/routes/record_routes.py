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

    appointment = session.get('last_appointment', {})
    return render_template('record.html', user=session['user'], appointment=appointment)

@record.route('/save_video', methods=['POST'])
def save_video():
    if 'user' not in session:
        return "Unauthorized", 403

    if 'video' not in request.files:
        return "No video file part", 400

    video = request.files['video']
    patient = request.form.get('patient', 'unknown')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{patient}_{timestamp}.webm"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    video.save(filepath)
    
    # --- AI Analysis Start ---
    try:
        from app.genai.video_agent import VideoAgent
    except ImportError:
        from genai.video_agent import VideoAgent
        
    agent = VideoAgent()
    print(f"Starting analysis for {filepath}...")
    result = agent.analyze_consultation(filepath)
    
    # Store result in session to display on next page (or return JSON if using AJAX)
    # Since the frontend uses fetch(), returning the URL to redirect to is better, 
    # OR we can just return the text and let frontend handle it.
    # But the current frontend just prints the response text.
    # Let's improve the frontend flow in the next step.
    # For now, let's save the result to a file or session and return a success message.
    
    session['last_analysis'] = {
        'patient': patient,
        'date': timestamp,
        'analysis': result.get('text', ''),
        'error': result.get('error')
    }
    
    return "Video uploaded and analyzed! Redirecting..."
    
@record.route('/analysis_result')
def analysis_result():
    if 'user' not in session or 'last_analysis' not in session:
        return redirect(url_for('auth.dashboard'))
        
    data = session['last_analysis']
    return render_template('analysis_result.html', 
                           patient=data['patient'], 
                           date=data['date'], 
                           analysis=data['analysis'],
                           error=data['error'])