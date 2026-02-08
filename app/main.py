from flask import Flask, render_template
from routes.auth_routes import auth
from routes.record_routes import record
from routes.video_view_routes import video_view
from routes.upload_routes import upload
from routes.appointment_routes import appointments
from routes.genai_routes import genai_bp

app = Flask(__name__)

# Secret key for session management (needed for flash messages, etc.)
app.secret_key = 'supersecretkey'  # Change this in production

# Register all blueprints
app.register_blueprint(auth)
app.register_blueprint(record)
app.register_blueprint(video_view)
app.register_blueprint(upload)
app.register_blueprint(appointments)
app.register_blueprint(genai_bp)

# Root route
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)