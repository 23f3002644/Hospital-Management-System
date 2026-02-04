from flask import current_app as app  # prosess called modulirisation
#from app import app   ( to avoid circular import)

from flask_security import current_user, auth_required, roles_required
#auth_required : For Authentication
#roles_required : For Authorization

@app.route('/admin_dashboard')
@auth_required('token')  # Protect this route, only accessible to authenticated users
@roles_required("admin") # Only users with 'admin' role can access
def admin_dashboard():
    user = current_user
    roles = current_user.roles

    return {"message": "Welcome to the Admin Dashboard",
            "email": user.email, "password": user.password, "active": user.active, "roles": [role.name for role in roles], "status_code": 200}

@app.route('/doctor_dashboard')
@auth_required('token')  # Protect this route, only accessible to authenticated users
@roles_required("doctor") # Only users with 'doctor' role can access
def doctor_dashboard():
    user = current_user
    roles = current_user.roles

    return {"message": "Welcome to the Doctor Dashboard",
            "email": user.email, "password": user.password, "active": user.active, "roles": [role.name for role in roles], "status_code": 200}

@app.route('/patient_dashboard')
@auth_required('token')  # Protect this route, only accessible to authenticated users
@roles_required("patient") # Only users with 'patient' role can access
def patient_dashboard():
    user = current_user
    roles = current_user.roles

    return {"message": "Welcome to the Patient Dashboard",
            "email": user.email, "password": user.password, "active": user.active, "roles": [role.name for role in roles], "status_code": 200}

