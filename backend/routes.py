from flask import current_app as app, request, jsonify # prosess called modulirisation
#from app import app   ( to avoid circular import)
from database import db
from flask_login import login_user
from flask_security import current_user, auth_required, roles_required, hash_password
from flask_security.utils import verify_password
#auth_required : For Authentication
#roles_required : For Authorization
from model import *
import json
from datetime import datetime, date, time


#login api route

@app.route("/api/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required", "status_code": 400})
    
    user = app.security.datastore.find_user(email=email)
    passing = verify_password(password, user.password) if user else False

    if user and passing:
        login_user(user)
        token = user.get_auth_token()
        return jsonify({"message": "Login successful", "token": token, "user_id": current_user.id, "status_code": 200})
    else:
        return jsonify({"message": "Invalid credentials", "status_code": 401})


@app.route("/api/register", methods=["POST"])
def register():
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    age = request.json.get("age")
    address = request.json.get("address")
    contact_number = request.json.get("contact_number")
    gender = request.json.get("gender")

    if app.security.datastore.find_user(email=email):
        return jsonify({"message": "User already exists", "status_code": 400})
    else:
        app.security.datastore.create_user(email=email, password=hash_password(password), roles=['patient']) #default role is patient
        patient = Patient(user_id=app.security.datastore.find_user(email=email).id, name=name, age=age, address=address, contact_number=contact_number, gender=gender)
        db.session.add(patient)
        db.session.commit()
        return jsonify({"message": "User registered successfully", "status_code": 201})

@app.route("/api/update_patient/<string:name>", methods=["PUT"])
@auth_required('token')
@roles_required("patient")
def update_patient(name):
    patient = Patient.query.filter_by(name=name).first()
    patient.name = request.json.get("name", patient.name)
    patient.age = request.json.get("age", patient.age)
    patient.address = request.json.get("address", patient.address)
    patient.contact_number = request.json.get("contact_number", patient.contact_number)
    db.session.commit()
    return jsonify({"message": "Patient updated successfully", "status_code": 200})

@app.route("/api/new_doctor", methods=["POST"])
@auth_required('token') 
@roles_required("admin")
def new_doctor():
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    age = request.json.get("age")
    address = request.json.get("address")
    contact_number = request.json.get("contact_number")
    gender = request.json.get("gender")
    specialty= request.json.get("specialty")
    department_name= request.json.get("department_name")
    description= request.json.get("description")

    if app.security.datastore.find_user(email=email):
        return jsonify({"message": "Doctor already exists", "status_code": 400})
    else:
        app.security.datastore.create_user(email=email, password=hash_password(password), roles=['doctor']) #default role is doctor
        doctor = Doctor(user_id=app.security.datastore.find_user(email=email).id, name=name, age=age, address=address, contact_number=contact_number, gender=gender, specialty=specialty, department_name=department_name, description=description)
        db.session.add(doctor)
        db.session.commit()
        return jsonify({"message": "Doctor registered successfully", "status_code": 201})

@app.route("/api/update_doctor/<string:name>", methods=["PUT"])
@auth_required('token') 
@roles_required("admin")
def update_doctor(name):
    
    doctor = Doctor.query.filter_by(name=name).first()
    doctor.name = request.json.get("name", doctor.name)
    doctor.age = request.json.get("age", doctor.age)
    doctor.address = request.json.get("address", doctor.address)
    doctor.contact_number = request.json.get("contact_number", doctor.contact_number)
    doctor.gender = request.json.get("gender", doctor.gender)
    doctor.specialty = request.json.get("specialty", doctor.specialty)
    doctor.department_name = request.json.get("department_name", doctor.department_name)
    doctor.description = request.json.get("description", doctor.description)


    db.session.commit()
    return jsonify({"message": "Doctor updated successfully", "status_code": 200})

@app.route("/api/delete_doctor/<string:name>", methods=["DELETE"])
@auth_required('token')
@roles_required("admin")
def delete_doctor(name):
    doctor = Doctor.query.filter_by(name=name).first()
    if doctor:
        db.session.delete(doctor)
        db.session.commit()

        his_user = app.security.datastore.find_user(id=doctor.user_id)
        if his_user:
            app.security.datastore.delete_user(his_user)
            db.session.commit()
        return jsonify({"message": "Doctor and associated user deleted successfully", "status_code": 200})
    
    else:
        return jsonify({"message": "Doctor not found", "status_code": 404})
    

@app.route("/api/delete_patient/<string:name>", methods=["DELETE"])
@auth_required('token')
@roles_required("admin")
def delete_patient(name):
    patient = Patient.query.filter_by(name=name).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()

        his_user = app.security.datastore.find_user(id=patient.user_id)
        if his_user:
            app.security.datastore.delete_user(his_user)
            db.session.commit()
        return jsonify({"message": "Patient and associated user deleted successfully", "status_code": 200})
    
    else:
        return jsonify({"message": "Patient not found", "status_code": 404})
    
    

@app.route("/api/new_department", methods=["POST"])
@auth_required('token') 
@roles_required("admin")
def new_department():
    name = request.json.get("name")
    overview = request.json.get("overview")

    if Departments.query.filter_by(name=name).first():
        return jsonify({"message": "Department already exists", "status_code": 400})
    else:
        department = Departments(name=name, overview=overview)
        db.session.add(department)
        db.session.commit()
        return jsonify({"message": "Department created successfully", "status_code": 201})

@app.route("/api/appointment", methods=["POST"])
@auth_required('token') 
@roles_required("patient")
def appointment():
    doctor = request.json.get("doctor")
    department_name = request.json.get("department_name")
    time = request.json.get("time")
    date = request.json.get("date")

    py_date = datetime.strptime(date, "%Y-%m-%d").date() # string → date
    py_time = datetime.strptime(time, "%H:%M").time() # string → time

    

    doctor_obj = Doctor.query.filter_by(name=doctor).first()
    patient_id = Patient.query.filter_by(user_id=current_user.id).first().id
    doctor_id = doctor_obj.id if doctor_obj else None
    if not doctor_obj:
        return jsonify({"message": "Doctor not found", "status_code": 404})

    appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, department_name=department_name, time=py_time, date=py_date)
    db.session.add(appointment)
    db.session.commit()
    return jsonify({"message": "Appointment created successfully", "status_code": 201})

@app.route("/api/cancel_appointment/<int:appointment_id>", methods=["PUT"])
@auth_required('token')
def cancel_appointment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if not appointment:
        return jsonify({"message": "Appointment not found", "status_code": 404})

    # Check role of current user
    if current_user.has_role("patient") or current_user.has_role("doctor"):
        current_user_id = current_user.id
        # Verify that the user is either the patient or the doctor associated with the appointment
        patient = Patient.query.filter_by(id=appointment.patient_id).first()
        doctor = Doctor.query.filter_by(id=appointment.doctor_id).first()
        if not (patient and patient.user_id == current_user_id) and not (doctor and doctor.user_id == current_user_id):
            return jsonify({"message": "Unauthorized", "status_code": 403})
        appointment.status = 'canceled'
        db.session.commit()
        return jsonify({"message": "Appointment cancelled successfully", "status_code": 200})
    else:
        return jsonify({"message": "Unauthorized", "status_code": 403})


@app.route("/api/treatment/<int:appointment_id>", methods=["POST"])    #Here Add the appointment
@auth_required('token') 
@roles_required("doctor")
def treatment(appointment_id):
    if request.method == "POST":
        
        diagnosis = request.json.get("diagnosis")
        test_done = request.json.get("test_done")
        prescription = request.json.get("prescription")
        medicines = request.json.get("medicines")
        visit_type = request.json.get("visit_type")
        notes = request.json.get("notes")

        doctor_user_id = current_user.id 
        doctor_name = Doctor.query.filter_by(user_id=doctor_user_id).first().name
        doctor_id = Doctor.query.filter_by(user_id=doctor_user_id).first().id
        
        appointment = Appointment.query.filter_by(id=appointment_id, doctor_id=doctor_id).first()
        
        if not appointment:
            return jsonify({"message": "Appointment not found","doctor_name": doctor_name, "status_code": 404})
        appointment_id = appointment.id

        patient_name = Patient.query.filter_by(id=appointment.patient_id).first().name
        department_name = appointment.department_name

        treatment = Treatment(appointment_id=appointment_id, department_name=department_name, patient_name=patient_name, doctor_name=doctor_name, diagnosis=diagnosis, 
                              test_done=test_done, prescription=prescription, medicines=medicines, visit_type=visit_type, notes=notes)
        db.session.add(treatment)
        db.session.commit()

        appointment.status = 'completed'
        db.session.commit()
        return jsonify({"message": "Treatment and Appointment status updated successfully", "status_code": 201})
    




@app.route('/api/admin_dashboard')
@auth_required('token')  # Protect this route, only accessible to authenticated users
@roles_required("admin") # Only users with 'admin' role can access
def admin_dashboard():
    user = current_user
    roles = current_user.roles
    user_id = current_user.id
    doctors = Doctor.query.all()
    doctor_list = []
    for doctor in doctors:
        doctor_data = {
            "name": doctor.name,
            "age": doctor.age,
            "gender": doctor.gender,
            "specialty": doctor.specialty,
            "department_name": doctor.department_name,
            "contact_number": doctor.contact_number,
            "address": doctor.address,
            "description": doctor.description
        }
        doctor_list.append(doctor_data)

    patients = Patient.query.all()
    patient_list = []
    for patient in patients:
        patient_data = {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "address": patient.address,
            "contact_number": patient.contact_number,
            "gender": patient.gender
        }
        patient_list.append(patient_data)  

    appointments = Appointment.query.all()
    appointment_list = []
    for appointment in appointments:
        appointment_data = {
            "id": appointment.id,
            "patient_id": Patient.query.filter_by(id=appointment.patient_id).first().name,  # patient_id is foreign key to Patient.id, but we need user_id for patient
            "doctor_name": Doctor.query.filter_by(id=appointment.doctor_id).first().name,  # doctor_id is foreign key to Doctor.id, but we need user_id for doctor
            "department_name": appointment.department_name,
            "date": appointment.date.strftime("%Y-%m-%d"),
            "time": appointment.time.strftime("%H:%M"),
            "status": appointment.status
        }
        appointment_list.append(appointment_data)  

    department = Departments.query.all()
    department_list = []
    for dept in department:
        dept_data = {
            "name": dept.name,
            "overview": dept.overview
        }
        department_list.append(dept_data)       

    return {"message": "Welcome to the Admin Dashboard","doctors": doctor_list, "patients": patient_list, "appointments": appointment_list, "departments": department_list, "status_code": 200}

@app.route('/api/patient_history/<string:name>')
@auth_required('token')  # Protect this route, only accessible to authenticated users

def patient_history(name):
    patient = Patient.query.filter_by(name=name).first()
    treatment = Treatment.query.filter_by(patient_name=patient.name).all()

    if not treatment:
        return {"message": "No treatment history found for the patient", "status_code": 404}

    treatment_list = []
    for treat in treatment:
        treat_data = {
            "doctor_name": treat.doctor_name,
            "department_name": treat.department_name,
            "diagnosis": treat.diagnosis,
            "test_done": treat.test_done,
            "prescription": treat.prescription,
            "medicines": treat.medicines,
            "visit_type": treat.visit_type,
        }
        treatment_list.append(treat_data)
    return {"treatments": treatment_list, "patient_name": patient.name, "status_code": 200}

@app.route('/api/doctor_dashboard')
@auth_required('token')  # Protect this route, only accessible to authenticated users
@roles_required("doctor") # Only users with 'doctor' role can access
def doctor_dashboard():
    user_id = current_user.id
    doctor_id = Doctor.query.filter_by(user_id=user_id).first().id
    appointments = Appointment.query.filter_by(status="booked", doctor_id=doctor_id).all()
    appointment_list = []
    patient_list = []
    for appointment in appointments:
        appointment_data = {
            "id": appointment.id,
            "patient_id": Patient.query.filter_by(id=appointment.patient_id).first().name,  # patient_id is foreign key to Patient.id, but we need user_id for patient
            "doctor_name": Doctor.query.filter_by(id=appointment.doctor_id).first().name,  # doctor_id is foreign key to Doctor.id, but we need user_id for doctor
            "department_name": appointment.department_name,
            "doctor_id": appointment.doctor_id,
            "date": appointment.date.strftime("%Y-%m-%d"),
            "time": appointment.time.strftime("%H:%M"),
            "status": appointment.status
        }
        patient_data ={
            "id":appointment.patient_id,
            "name": Patient.query.filter_by(id=appointment.patient_id).first().name,
        }
        patient_list.append(patient_data)
        appointment_list.append(appointment_data)

    return {"message": "Welcome to the Doctor Dashboard", "appointments": appointment_list, "patients": patient_list, "status_code": 200}

@app.route('/api/patient_dashboard')
@auth_required('token')  # Protect this route, only accessible to authenticated users
@roles_required("patient") # Only users with 'patient' role can access
def patient_dashboard():
    user_id = current_user.id
    roles = current_user.roles
    patient_id = Patient.query.filter_by(user_id=user_id).first().id

    departments = Departments.query.all()
    department_list = []
    for dept in departments:
        dept_data = {
            "name": dept.name,
            "overview": dept.overview
        }
        department_list.append(dept_data)

    appointments = Appointment.query.filter_by(patient_id=patient_id,status="booked").all() 
    appointment_list = []
    for appointment in appointments:
        appointment_data = {
            "doctor_name": Doctor.query.filter_by(id=appointment.doctor_id).first().name,  # doctor_id is foreign key to Doctor.id, but we need user_id for doctor
            "department_name": appointment.department_name,
            "date": appointment.date.strftime("%Y-%m-%d"),
            "time": appointment.time.strftime("%H:%M"),
        }
        appointment_list.append(appointment_data)   

    return {"message": "Welcome to the Patient Dashboard", "departments": department_list, "appointments": appointment_list, "status_code": 200}

@app.route('/api/department_doctors/<string:department_name>')
@auth_required('token')  # Protect this route, only accessible to authenticated users
def department_doctors(department_name):
    department = Departments.query.filter_by(name=department_name).first()
    depart_views = {
        "name": department.name,
        "overview": department.overview
    }
    doctors = Doctor.query.filter_by(department_name=department_name).all()
    doctor_list = []
    for doctor in doctors:
        doctor_data = {
            "name": doctor.name,
            "gender":doctor.gender,
            "specialty": doctor.specialty,
            "description": doctor.description
        }
        doctor_list.append(doctor_data)
    return {"doctors": doctor_list,"department_views": depart_views, "status_code": 200}

