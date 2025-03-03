import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Load environment variables
load_dotenv()

app = Flask(__name__)

#   PostgreSQL Connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "postgresql://postgres:51214@localhost/postgres"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecret")

db = SQLAlchemy(app)

#   Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect if not logged in

#   Logging Setup
logging.basicConfig(
    filename="app.log",  # Log file
    level=logging.INFO,  # Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

logger.info("User Service Started")
