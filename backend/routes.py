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
    
    user = app.security.datastore.find_user(email=email)
    passing = verify_password(password, user.password) if user else False

    if user and passing:
        login_user(user)
        token = user.get_auth_token()
        if not user.active:
            return jsonify(message="User is blacklisted"), 400
        current_user_id= current_user.id
        type_id = UserRoles.query.filter_by(user_id=current_user.id).first().role_id
        user_type= Role.query.filter_by(id=type_id).first().name
        if(user_type=='admin'):
            name = "Admin"
            id = current_user.id
        elif(user_type=='doctor'):
            name = Doctor.query.filter_by(user_id = current_user_id).first().name
            id = Doctor.query.filter_by(user_id = current_user_id).first().id
        else:
            name = Patient.query.filter_by(user_id= current_user_id).first().name
            id = Patient.query.filter_by(user_id= current_user_id).first().id
        return jsonify(token=token, user_type=user_type, current_user_id=current_user_id, name=name, id=id)
    else:
        return jsonify(message= "Invalid credentials"), 400

@app.route("/api/blacklist_patient/<int:patient_id>", methods=["PUT"])
@auth_required('token') 
@roles_required("admin")
def blacklist_patient(patient_id):
    user = app.security.datastore.find_user(id=Patient.query.filter_by(id=patient_id).first().user_id)
    if user:
        user.active = False
        db.session.commit()
        return jsonify(message="Patient blacklisted successfully", status_code=200)
    else:
        return jsonify(message="Patient not found", status_code=404)
    
@app.route("/api/unblacklist_patient/<int:patient_id>", methods=["PUT"])
@auth_required('token')
@roles_required("admin")
def unblacklist_patient(patient_id):
    user = app.security.datastore.find_user(id=Patient.query.filter_by(id=patient_id).first().user_id)
    if user:
        user.active = True
        db.session.commit()
        return jsonify(message="Patient unblacklisted successfully", status_code=200)
    else:
        return jsonify(message="Patient not found", status_code=404)

        
    
@app.route("/api/blacklist_doctor/<int:doctor_id>", methods=["PUT"])    
@auth_required('token') 
@roles_required("admin")
def blacklist_doctor(doctor_id):
    user = app.security.datastore.find_user(id=Doctor.query.filter_by(id=doctor_id).first().user_id)
    if user:
        user.active = False
        db.session.commit()
        return jsonify(message="Doctor blacklisted successfully", status_code=200)
    else:
        return jsonify(message="Doctor not found", status_code=404)
    
@app.route("/api/unblacklist_doctor/<int:doctor_id>", methods=["PUT"])
@auth_required('token')
@roles_required("admin")
def unblacklist_doctor(doctor_id):
    user = app.security.datastore.find_user(id=Doctor.query.filter_by(id=doctor_id).first().user_id)
    if user:
        user.active = True
        db.session.commit()
        return jsonify(message="Doctor unblacklisted successfully", status_code=200)
    else:
        return jsonify(message="Doctor not found", status_code=404)    

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
        return jsonify(message= "User already exists"), 400
    else:
        app.security.datastore.create_user(email=email, password=hash_password(password), roles=['patient']) #default role is patient
        patient = Patient(user_id=app.security.datastore.find_user(email=email).id, name=name, age=age, address=address, contact_number=contact_number, gender=gender)
        db.session.add(patient)
        db.session.commit()
        return jsonify(message ="User registered successfully")

@app.route("/api/update_patient/<int:id>", methods=["PUT"])
@auth_required('token')
@roles_required("patient")
def update_patient(id):
    patient = Patient.query.filter_by(id=id).first()
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

@app.route("/api/update_doctor/<int:doctor_id>", methods=["PUT"])
@auth_required('token') 
@roles_required("admin")
def update_doctor(doctor_id):
    
    doctor = Doctor.query.filter_by(id=doctor_id).first()
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

@app.route("/api/delete_doctor/<int:doctor_id>", methods=["DELETE"])
@auth_required('token')
@roles_required("admin")
def delete_doctor(doctor_id):
    doctor = Doctor.query.filter_by(id=doctor_id).first()
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
    

@app.route("/api/delete_patient/<int:patient_id>", methods=["DELETE"])
@auth_required('token')
@roles_required("admin")
def delete_patient(patient_id):
    patient = Patient.query.filter_by(id=patient_id).first()
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
    slot = AvailableSlot.query.filter_by(doctor_id=doctor_id, date=py_date, start_time=py_time,is_available=True).first()
    slot.status = False
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
        user_active = app.security.datastore.find_user(id=Doctor.query.filter_by(id=doctor.id).first().user_id).active
        doctor_data = {
            "id": doctor.id,
            "name": doctor.name,
            "age": doctor.age,
            "gender": doctor.gender,
            "specialty": doctor.specialty,
            "department_name": doctor.department_name,
            "contact_number": doctor.contact_number,
            "address": doctor.address,
            "description": doctor.description,
            "active": user_active
        }
        doctor_list.append(doctor_data)

    patients = Patient.query.all()
    patient_list = []
    
    for patient in patients:
        user_active = app.security.datastore.find_user(id=Patient.query.filter_by(id=patient.id).first().user_id).active
        patient_data = {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "address": patient.address,
            "contact_number": patient.contact_number,
            "gender": patient.gender,
            "active": user_active
        }
        patient_list.append(patient_data)  

    appointments = Appointment.query.all()
    appointment_list = []
    for appointment in appointments:
        appointment_data = {
            "id": appointment.id,
            "patient_name": Patient.query.filter_by(id=appointment.patient_id).first().name if Patient.query.filter_by(id=appointment.patient_id).first() else None,
            "doctor_name": Doctor.query.filter_by(id=appointment.doctor_id).first().name if Doctor.query.filter_by(id=appointment.doctor_id).first() else None,
            "department_name": appointment.department_name,
            "date": appointment.date.strftime("%Y-%m-%d"),
            "time": appointment.time.strftime("%H:%M"),
            "status": appointment.status,
            "patient_id": appointment.patient_id,
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

    treatment = Treatment.query.all()
    treatment_list = []
    for treat in treatment:
        treat_data = {
            "doctor_name": treat.doctor_name,
            "patient_name": treat.patient_name,
            "department_name": treat.department_name,
            "diagnosis": treat.diagnosis,
            "test_done": treat.test_done,
            "prescription": treat.prescription,
            "medicines": treat.medicines,
            "visit_type": treat.visit_type,
            "notes": treat.notes,
            "date": Appointment.query.filter_by(id=treat.appointment_id).first().date.strftime("%Y-%m-%d") if Appointment.query.filter_by(id=treat.appointment_id).first() else None,
            "time": Appointment.query.filter_by(id=treat.appointment_id).first().time.strftime("%H:%M") if Appointment.query.filter_by(id=treat.appointment_id).first() else None
        }
        treatment_list.append(treat_data)           

    return {"message": "Welcome to the Admin Dashboard","doctors": doctor_list, "patients": patient_list, "appointments": appointment_list, "departments": department_list, "treatments": treatment_list, "status_code": 200}

@app.route('/api/patient_history/<int:id>')
@auth_required('token')  # Protect this route, only accessible to authenticated users

def patient_history(id):
    patient = Patient.query.filter_by(id=id).first()
    patient_name = patient.name
    treatment = Treatment.query.filter_by(patient_name=patient_name).all()

    if not treatment:
        return {"message": "No treatment history found for the patient","patient_name": patient.name, "patient_gender": patient.gender, "patient_age": patient.age, "status_code": 404}

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
            "date": Appointment.query.filter_by(id=treat.appointment_id).first().date.strftime("%Y-%m-%d") if Appointment.query.filter_by(id=treat.appointment_id).first() else None,
            "time": Appointment.query.filter_by(id=treat.appointment_id).first().time.strftime("%H:%M") if Appointment.query.filter_by(id=treat.appointment_id).first() else None
        }
        treatment_list.append(treat_data)
    return {"treatments": treatment_list, "patient_name": patient_name, "patient_gender": patient.gender, "patient_age": patient.age, "message": "Treatment history retrieved successfully", "status_code": 200}

@app.route('/api/history_by_doctor/<int:id>')
@auth_required('token')  # Protect this route, only accessible to authenticated users

def history(id):
    patient = Patient.query.filter_by(id=id).first()
    patient_name = patient.name
    treatment = Treatment.query.filter_by(patient_name=patient_name).all()

    if not treatment:
        return {"message": "No treatment history found for the patient","patient_name": patient.name, "patient_gender": patient.gender, "patient_age": patient.age, "status_code": 404}

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
            "date": Appointment.query.filter_by(id=treat.appointment_id).first().date.strftime("%Y-%m-%d") if Appointment.query.filter_by(id=treat.appointment_id).first() else None,
            "time": Appointment.query.filter_by(id=treat.appointment_id).first().time.strftime("%H:%M") if Appointment.query.filter_by(id=treat.appointment_id).first() else None
        }
        treatment_list.append(treat_data)
    return {"treatments": treatment_list, "patient_name": patient_name, "patient_gender": patient.gender, "patient_age": patient.age, "message": "Treatment history retrieved successfully", "status_code": 200}


@app.route('/api/doctor_dashboard')
@auth_required('token')  # Protect this route, only accessible to authenticated users
@roles_required("doctor") # Only users with 'doctor' role can access
def doctor_dashboard():
    user_id = current_user.id
    doctor_id = Doctor.query.filter_by(user_id=user_id).first().id
    appointments = Appointment.query.filter_by(status="booked", doctor_id=doctor_id).order_by(Appointment.date, Appointment.time).all()
    
    appointment_list = []
    patient_ids = set()

    
    for appointment in appointments:
        patient = Patient.query.filter_by(id=appointment.patient_id).first()
        doctor = Doctor.query.filter_by(id=appointment.doctor_id).first()
        appointment_data = {
            "id": appointment.id,
            "patient_name": patient.name if patient else "Unknown",
            "patient_id": appointment.patient_id,
            "doctor_name": doctor.name if patient else "Unknown",
            "department_name": appointment.department_name,
            "doctor_id": appointment.doctor_id,
            "date": appointment.date.strftime("%Y-%m-%d"),
            "time": appointment.time.strftime("%H:%M"),
            "status": appointment.status
        }
        appointment_list.append(appointment_data)
        patient_ids.add(appointment.patient_id)

    patient_list = [] 
    for patient_id in patient_ids:
        patient = Patient.query.filter_by(id=patient_id).first()
        if patient:  
            patient_list.append({
                "id": patient.id,
                "name": patient.name
            }) 

    return {"message": "Welcome to the Doctor Dashboard", "appointments": appointment_list, "unique_patients": patient_list, "status_code": 200}

@app.route('/api/patient_dashboard')
@auth_required('token')  # Protect this route, only accessible to authenticated users
@roles_required("patient") # Only users with 'patient' role can access
def patient_dashboard():
    user_id = current_user.id
    roles = current_user.roles
    patient = Patient.query.filter_by(user_id=user_id).first()
    patient_details = {
        "name": patient.name,
        "age": patient.age,
        "address": patient.address,
        "contact_number": patient.contact_number,
    }
    patient_id = Patient.query.filter_by(user_id=user_id).first().id

    departments = Departments.query.all()
    department_list = []
    for dept in departments:
        dept_data = {
            "id": dept.id,
            "name": dept.name,
            "overview": dept.overview
        }
        department_list.append(dept_data)

    appointments = Appointment.query.filter_by(patient_id=patient_id,status="booked").all() 
    appointment_list = []
    for appointment in appointments:
        appointment_data = {
            "id": appointment.id,
            "doctor_name": Doctor.query.filter_by(id=appointment.doctor_id).first().name,  # doctor_id is foreign key to Doctor.id, but we need user_id for doctor
            "department_name": appointment.department_name,
            "date": appointment.date.strftime("%Y-%m-%d"),
            "time": appointment.time.strftime("%H:%M"),
        }
        appointment_list.append(appointment_data)   

    doctors = Doctor.query.all()
    doctor_list = []
    for doctor in doctors:
        doctor_data = {
            "id":doctor.id,
            "name": doctor.name,
            "age": doctor.age,
            "gender": doctor.gender,
            "specialty": doctor.specialty,
            "description": doctor.description,
            "department_name": doctor.department_name,
            "contact_number": doctor.contact_number,
            "address": doctor.address
        }
        doctor_list.append(doctor_data)


    return {"message": "Welcome to the Patient Dashboard", "departments": department_list, "appointments": appointment_list, "patient_details": patient_details, "doctors": doctor_list, "status_code": 200}

@app.route('/api/department_doctors/<int:department_id>')
@auth_required('token')  # Protect this route, only accessible to authenticated users
def department_doctors(department_id):
    department = Departments.query.filter_by(id=department_id).first()
    depart_views = {
        "name": department.name,
        "overview": department.overview
    }
    doctors = Doctor.query.filter_by(department_name=department.name).all()
    doctor_list = []
    for doctor in doctors:
        doctor_data = {
            "id": doctor.id,
            "name": doctor.name
            # "gender":doctor.gender,
            # "specialty": doctor.specialty,
            # "description": doctor.description
        }
        doctor_list.append(doctor_data)
    return {"doctors": doctor_list,"department_views": depart_views, "status_code": 200}

@app.route('/api/doctor_details/<int:id>')
@auth_required('token')  # Protect this route, only accessible to authenticated users
def doctor_details(id):
    doctor = Doctor.query.filter_by(id=id).first()
    dept_id = Departments.query.filter_by(name=doctor.department_name).first().id if Departments.query.filter_by(name=doctor.department_name).first() else None
    if not doctor:
        return {"message": "Doctor not found", "status_code": 404}
    doctor_data = {
        "id": doctor.id,
        "name": doctor.name,
        "age": doctor.age,
        "gender": doctor.gender,
        "specialty": doctor.specialty,
        "description": doctor.description,
        "department_name": doctor.department_name,
        "contact_number": doctor.contact_number,
        "address": doctor.address
    }
    return {"doctor": doctor_data, "status_code": 200, "dept_id": dept_id}


@app.route('/api/doctor_available_slots/<int:doctor_id>', methods=["GET"])
@auth_required('token')
def doctor_available_slots(doctor_id):
    date_param = request.args.get('date')
    
    query = AvailableSlot.query.filter_by(doctor_id=doctor_id, is_available=True, status=True)
    
    if date_param:
        py_date = datetime.strptime(date_param, "%Y-%m-%d").date()
        query = query.filter(AvailableSlot.date == py_date)
    
    # ✅ DISTINCT query - removes duplicates
    available_slots = query.distinct(AvailableSlot.start_time).all()
    
    slots_list = []
    for slot in available_slots:
        slots_list.append({
            "date": slot.date.strftime("%Y-%m-%d"),
            "start_time": slot.start_time.strftime("%H:%M"),
            "is_available": slot.is_available
        })
    
    return {"available_slots": slots_list}


@app.route('/api/add_available_slot/<int:doctor_id>', methods=["POST"])
@auth_required('token')  # Protect this route, only accessible to authenticated users
@roles_required("doctor") # Only users with 'doctor' role can access
def add_available_slot(doctor_id):
    doctor = Doctor.query.filter_by(id=doctor_id).first()
    if not doctor:
        return {"message": "Doctor not found", "status_code": 404}
    
    data = request.get_json()
    for date_str, periods in data.items():
        py_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        for period, slots in periods.items():

            for time_str, is_available in slots.items():
                slot = AvailableSlot.query.filter_by(doctor_id=doctor_id, date=py_date, start_time=datetime.strptime(time_str, "%H:%M").time()).first()
                if slot:
                    slot.is_available = is_available
                else:
                    new_slot = AvailableSlot(doctor_id=doctor_id, date=py_date, start_time=datetime.strptime(time_str, "%H:%M").time(), is_available=is_available)
                    db.session.add(new_slot)
    db.session.commit()

    # date = request.json.get("date")
    # start_time = request.json.get("start_time")

    # py_date = datetime.strptime(date, "%Y-%m-%d").date() # string → date
    # py_time = datetime.strptime(start_time, "%H:%M").time() # string → time

    # new_slot = AvailableSlot(doctor_id=doctor_id, date=py_date, start_time=py_time)
    # db.session.add(new_slot)
    # db.session.commit()

    return {"message": "Weekly availability updated successfully", "status_code": 201}