# Base configuration class, common settings to all referenced
import os
from dotenv import load_dotenv

load_dotenv()

class Baseconfig:            
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

# Development configuration class
# Local SQLite database for development

class LocalDevelopmentConfig(Baseconfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'
    DEBUG = True 

    #configurtion for security
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = "argon2"
    WTF_CSRF_ENABLED = False #only for forms
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"



# Production configuration class
# Placeholder for production database URI

class ProductionConfig(Baseconfig):
    DEBUG = False      