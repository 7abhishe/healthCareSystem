from flask import session
from flask import Blueprint, render_template, request, redirect, url_for, flash
import csv
import os

appointments = Blueprint('appointments', __name__, url_prefix='/appointments')
APPOINTMENT_FILE = 'appointments.csv'


@appointments.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'user' not in session:
        flash("Please login to book an appointment.", "warning")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        data = [
            session['user']['name'],  # Use logged-in patient's name
            request.form['doctor'],
            request.form['date'],
            request.form['slot']
        ]
        with open(APPOINTMENT_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        flash("Appointment booked!", "success")
        return redirect(url_for('appointments.book_appointment'))
    
    return render_template('book_appointment.html')