from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import csv
import os

auth = Blueprint('auth', __name__)
USER_FILE = 'users.csv'

# Ensure CSV exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['role', 'name', 'email', 'password'])

@auth.route('/register', methods=['GET', 'POST'])
def register():
    role_filter = request.args.get('role') # ?role=Doctor or ?role=Patient
    
    if request.method == 'POST':
        role = request.form['role']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        # Check if email exists
        with open(USER_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) > 2 and row[2] == email:
                    flash("Email already registered.", "error")
                    return redirect(url_for('auth.register'))

        with open(USER_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([role, name, email, password])
            
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('auth.login'))
        
    return render_template('register.html', role_filter=role_filter)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = None
        with open(USER_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == email and row['password'] == password:
                    user = row
                    break
        
        if user:
            session['user'] = user
            flash("Login successful!", "success")
            if user['role'] == 'Doctor':
                 return redirect(url_for('auth.dashboard')) # Doctors might need a specific dashboard later
            return redirect(url_for('appointments.book_appointment'))
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