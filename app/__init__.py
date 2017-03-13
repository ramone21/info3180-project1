from flask import Flask
from flask_sqlalchemy import SQLAlchemy

SECRET_KEY = 'Sup3r$3cretkey'
UPLOAD_FOLDER = '/app/static/uploads'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project1:2468@localhost/project1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning
db = SQLAlchemy(app)

app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from app import views
