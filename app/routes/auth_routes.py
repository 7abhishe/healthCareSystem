from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth = Blueprint('auth', __name__)
users = []  # In-memory storage (can replace with CSV or DB)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form['role']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        users.append({'role': role, 'name': name, 'email': email, 'password': password})
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            session['user'] = user
            flash("Login successful!", "success")
            return redirect(url_for('appointments.book_appointment'))  # 🔁 Go to appointment page
        else:
            flash("Invalid credentials.", "error")
    return render_template('login.html')

@auth.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', user=session['user'])

@auth.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth.login'))