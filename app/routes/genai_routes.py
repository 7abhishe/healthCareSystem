from flask import Blueprint, render_template, request, session, redirect, url_for
from app.genai.emergency_agent import EmergencyAgent

genai_bp = Blueprint('genai', __name__)
agent = EmergencyAgent()

@genai_bp.route('/emergency', methods=['GET', 'POST'])
def emergency():
    # Allow anonymous access for emergency? Or require login?
    # Requirement implied "accessible through the genai based model", usually emergency is public or quick access.
    # But let's keep it overlapping with logged in user context if available, or just open.
    # For now, let's keep it simple: anyone can access.
    
    if 'chat_history' not in session:
        session['chat_history'] = []
        
    if request.method == 'POST':
        user_input = request.form['user_input']
        response = agent.get_response(user_input)
        
        # Append to session history
        # We need to re-assign session['chat_history'] to trigger save
        history = session['chat_history']
        history.append({'type': 'user', 'sender': 'You', 'text': user_input})
        history.append({'type': 'ai', 'sender': 'AI', 'text': response})
        session['chat_history'] = history
        
    return render_template('emergency.html', chat_history=session.get('chat_history', []))
