import datetime
from celery import shared_task
from flask import current_app as app, request, jsonify 
from flask import Flask, jsonify
from jinja2 import Template
import asyncio

import requests

# from flask_cors import CORS
from database import *
from model import *
from mail import send_email

import csv

# task-1 - Download CSV report for the patient
# Patient trigger async job

@shared_task(ignore_results=False, name="download_csv_report")
def csv_report(patient_id):
    patient = Patient.query.filter_by(id=patient_id).first()
    if not patient:
        return "Patient not found"
    
    patient_name = patient.name
    card_details = Treatment.query.filter_by(patient_name=patient_name).all()
    csv_file_name = f"card_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(f'static/{csv_file_name}', 'w', newline="") as csvfile:
        sr_no = 1
        card_csv = csv.writer(csvfile, delimiter=',')
        card_csv.writerow(['Sr No.', 'Doctor Name', 'Department name', 'Diagnosis', 'Test Done', 'Prescription', 'Medicines', 'Notes', 'Date'])
        
        for c in card_details:
            appointment = Appointment.query.filter_by(id=c.appointment_id).first()  # ✅ .first()
            if appointment:  # ✅ Null check
                card_csv.writerow([
                    sr_no, c.doctor_name, c.department_name, c.diagnosis, 
                    c.test_done, c.prescription, c.medicines, c.notes, appointment.date
                ])
                sr_no += 1
    
    return csv_file_name




#task-2 - Monthly report
#scheduled job via crontab

@shared_task(ignore_results=False, name="monthly_report")
def monthly_report():
    doctors_list = []
    users = Doctor.query.all()
    
    for user in users:
        doc_record = Doctor.query.filter_by(id=user.id).first()  # ✅ Use user.id
        doc = app.security.datastore.find_user(id=doc_record.user_id)
        if not doc:
            continue
            
        user_data = {
            'username': user.name,
            'email': doc.email,
            'details': []
        }
        
        treatments = Treatment.query.filter_by(doctor_name=user.name).all()
        for treat in treatments:
            appointment = Appointment.query.filter_by(id=treat.appointment_id).first()
            if appointment:
                user_data['details'].append({
                    "Patient_name": treat.patient_name,
                    "diagnosis": treat.diagnosis,
                    "test_done": treat.test_done,
                    "prescription": treat.prescription,
                    "medicines": treat.medicines,
                    "notes": treat.notes,
                    "Date": appointment.date
                })
        
        doctors_list.append(user_data)
        
        # Email template fix: user_data → user_data (singular), add missing </th>
        mail_template = """
        <h3>Dear {{ username }}</h3>  <!-- Fixed: user_data.username -->
        <p>Please have a look on your treatment of this month</p>
        <table>
            <tr>
                <th>Patient name</th>
                <th>Diagnosis</th>
                <th>Test Done</th>
                <th>Prescription</th>
                <th>Medicines</th>
                <th>Notes</th>
                <th>Date</th>
            </tr>
            {% for detail in details %}  <!-- Fixed: user_data.details -->
            <tr>
                <td>{{detail.Patient_name}}</td>
                <td>{{detail.diagnosis}}</td>
                <td>{{detail.test_done}}</td>
                <td>{{detail.prescription}}</td>
                <td>{{detail.medicines}}</td>
                <td>{{detail.notes}}</td>
                <td>{{detail.Date}}</td>
            </tr>
            {% endfor %}
        </table>
        <p>Regards<br>Ayurveda Hospital</p>
        """
        message = Template(mail_template).render(**user_data)  # ✅ Unpack dict
        send_email(doc.email, "Monthly card detail Report - E card", message)  # ✅ doc.email
    
    return "Monthly reports sent"



#task-3 - daily reminder (Backend async job)
# Appointment alert on the day and treatment done alert on the day

@shared_task(ignore_results = False, name = "generate_msg")
def generate_msg(username, a_date, a_time, doctor_name):
    text = f"Hi {username}, your Appointment has been booked on {a_date} at {a_time} to {doctor_name}. For  more information, Please check the app at http://127.0.0.1:5173"
    response = requests.post("https://chat.googleapis.com/v1/spaces/AAQACE-t-VI/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=sowQTT-JSnLp8QKsCNF-gm-juG7j9g-sGjWxGJPELL4", json = {"text": text})
    print(response.status_code)
    return "The delivery is sent to user"

