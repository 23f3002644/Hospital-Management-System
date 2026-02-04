from flask import Flask, jsonify
from flask_cors import CORS
from database import db
from model import *
from config import LocalDevelopmentConfig #import the config class
from dotenv import load_dotenv
from flask_security import Security, SQLAlchemyUserDatastore, hash_password





def create_app():
    app = Flask(__name__)
    load_dotenv()  # Load environment variables from .env file
    
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, origins="*")
    db.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)   #way to connect the database to flask security

    app.app_context().push()
    return app

app = create_app()

with app.app_context():
    db.create_all()

    app.security.datastore.find_or_create_role(name='admin', description='This is Administrator')
    app.security.datastore.find_or_create_role(name='patient', description='This is Patient User')
    app.security.datastore.find_or_create_role(name='doctor', description='This is Doctor User')
    db.session.commit()

    if not app.security.datastore.find_user(email="admin@gmail.com"):
        app.security.datastore.create_user(email="admin@gmail.com", password=hash_password("123456"), roles=['admin', 'doctor', 'patient'])
    db.session.commit()

    if not app.security.datastore.find_user(email="akash@gmail.com"):
        app.security.datastore.create_user(email="akash@gmail.com", password=hash_password("123456"), roles=['patient'])
    db.session.commit()

    if not app.security.datastore.find_user(email="amit@gmail.com"):
        app.security.datastore.create_user(email="amit@gmail.com", password=hash_password("123456"), roles=['doctor'])
    db.session.commit()

from routes import *    




if (__name__ == "__main__"):
    app.run(debug=True)
