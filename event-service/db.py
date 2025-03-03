from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Use environment variables for security
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://postgres:51214@localhost/Event-Service")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
