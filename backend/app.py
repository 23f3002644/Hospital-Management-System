from flask import Flask, jsonify
from flask_cors import CORS
from database import *
from model import *
from config import LocalDevelopmentConfig #import the config class
from dotenv import load_dotenv
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from celery_init import celery_init_app
from celery.schedules import crontab


def create_app():
    app = Flask(__name__)
    load_dotenv()  # Load environment variables from .env file
    
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, origins="*")
    db.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)   #way to connect the database to flask security

    #cache
    # cache.init_app(app)

    app.app_context().push()
    return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

#mailhog periodly sent interval of 2 minutes

@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute = '*/2'),
        monthly_report.s(),
    )

def init_db():
    with app.app_context():
        db.session.execute(db.text("PRAGMA journal_mode=WAL;"))
        db.session.execute(db.text("PRAGMA synchronous=NORMAL;"))
        db.create_all()

        app.security.datastore.find_or_create_role(name='admin', description='This is Administrator')
        app.security.datastore.find_or_create_role(name='patient', description='This is Patient User')
        app.security.datastore.find_or_create_role(name='doctor', description='This is Doctor User')
        db.session.commit()

        if not app.security.datastore.find_user(email="admin@gmail.com"):
            app.security.datastore.create_user(email="admin@gmail.com", password=hash_password("123456"), roles=['admin'])
        db.session.commit()


from routes import *    




if (__name__ == "__main__"):
    init_db()
    app.run(debug=True)
