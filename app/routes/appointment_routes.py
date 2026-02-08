from flask import session
from flask import Blueprint, render_template, request, redirect, url_for, flash
import csv
import os

appointments = Blueprint('appointments', __name__, url_prefix='/appointments')
APPOINTMENT_FILE = 'appointments.csv'
DOCTOR_FILE = 'app/doctors.csv' # Assuming running from root, careful with path
if not os.path.exists(DOCTOR_FILE):
    DOCTOR_FILE = 'doctors.csv' # Fallback if running from app/

def get_doctors():
    doctors = []
    if os.path.exists(DOCTOR_FILE):
        with open(DOCTOR_FILE, 'r') as f:
            reader = csv.reader(f)
            doctors = [row[0] for row in reader if row]
    return doctors

def is_slot_available(doctor, date, slot):
    if not os.path.exists(APPOINTMENT_FILE):
        return True
    with open(APPOINTMENT_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            # row: [Patient, Doctor, Date, Slot]
            if len(row) >= 4 and row[1] == doctor and row[2] == date and row[3] == slot:
                return False
    return True

@appointments.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if 'user' not in session:
        flash("Please login to book an appointment.", "warning")
        return redirect(url_for('auth.login'))

    doctors = get_doctors()
    
    if request.method == 'POST':
        doctor = request.form['doctor']
        date = request.form['date']
        slot = request.form['slot']
        
        if not is_slot_available(doctor, date, slot):
            flash(f"Slot {slot} for {doctor} on {date} is already booked. Please choose another.", "error")
            return redirect(url_for('appointments.book_appointment'))

        data = [
            session['user']['name'],
            doctor,
            date,
            slot
        ]
        
        # Ensure file exists
        if not os.path.exists(APPOINTMENT_FILE):
            with open(APPOINTMENT_FILE, 'w') as f: pass

        with open(APPOINTMENT_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        
        # Save last appointment in session for record page
        session['last_appointment'] = {'doctor': doctor, 'date': date, 'slot': slot}
        
        flash("Appointment booked successfully!", "success")
        return redirect(url_for('appointments.book_appointment'))
    
    return render_template('book_appointment.html', doctors=doctors)

@appointments.route('/my_appointments')
def my_appointments():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
        
    user_appointments = []
    if os.path.exists(APPOINTMENT_FILE):
        with open(APPOINTMENT_FILE, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 4 and row[0] == session['user']['name']:
                    user_appointments.append({'doctor': row[1], 'date': row[2], 'slot': row[3]})
                    
    return render_template('my_appointments.html', appointments=user_appointments)

@appointments.route('/reschedule', methods=['GET', 'POST'])
def reschedule():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        old_doctor = request.form['old_doctor']
        old_date = request.form['old_date']
        old_slot = request.form['old_slot']
        
        new_slot = request.form['new_slot']
        
        if not is_slot_available(old_doctor, old_date, new_slot):
             flash("New slot is not available.", "error")
             return redirect(url_for('appointments.my_appointments'))
             
        # Read all, replace, write back
        rows = []
        with open(APPOINTMENT_FILE, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            
        updated = False
        with open(APPOINTMENT_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in rows:
                if (not updated and len(row) >= 4 and 
                    row[0] == session['user']['name'] and 
                    row[1] == old_doctor and 
                    row[2] == old_date and 
                    row[3] == old_slot):
                    
                    row[3] = new_slot
                    updated = True
                writer.writerow(row)
                
        flash("Appointment rescheduled!", "success")
        return redirect(url_for('appointments.my_appointments'))
        
    return redirect(url_for('appointments.my_appointments'))