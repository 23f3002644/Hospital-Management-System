from database import db
from datetime import datetime,timezone
from flask_security.core import UserMixin, RoleMixin

class BaseModel(db.Model):
    __abstract__ = True   # This tells SQLAlchemy not to create a table for this model
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class User(BaseModel, UserMixin):
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fs_uniquifier = db.Column(db.String(10000), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    roles = db.relationship('Role', secondary='user_roles', backref="users")   #User => user, Role => role, UserRoles => user_roles

class Role(BaseModel, RoleMixin):
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class UserRoles(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))    

class Patient(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50),nullable=False, default='patient')  # 'patient' or 'admin'
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

class Doctor(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name= db.Column(db.String(100), nullable=False)
    specialty= db.Column(db.String(100), nullable=False)
    department_name= db.Column(db.String(100), db.ForeignKey('departments.name'), nullable=False)
    contact_number= db.Column(db.String(15), nullable=False)
    address= db.Column(db.String(200), nullable=False)
    description= db.Column(db.Text, nullable=True)
    dept = db.relationship('Departments', backref=db.backref('doctor', lazy=True))

class Appointment(BaseModel):
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'),nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'),nullable=False)
    department_name = db.Column(db.String(100),db.ForeignKey('departments.name'), nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='booked')  # 'booked', 'completed', 'canceled' 

class Departments(BaseModel):
    name = db.Column(db.String(100), unique=True, nullable=False)
    overview = db.Column(db.Text, nullable=False)    

class Treatment(BaseModel):
    appointment_id = db.Column(db.Integer,db.ForeignKey('appointment.id'), nullable=False)
    department_name = db.Column(db.String(100),db.ForeignKey('departments.name'), nullable=False)
    patient_name = db.Column(db.String(100),db.ForeignKey('patient.name'), nullable=False)
    doctor_name = db.Column(db.String(100),db.ForeignKey('doctor.name'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    test_done = db.Column(db.Text, nullable=True)
    prescription = db.Column(db.Text, nullable=False)
    medicines = db.Column(db.Text, nullable=True)
    visit_type = db.Column(db.String(50), nullable=False)  # 'in-person' or 'outpatient'
    notes = db.Column(db.Text, nullable=True)
    
    