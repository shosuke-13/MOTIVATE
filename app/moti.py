from flask import Flask,render_template,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motivation.db'
db = SQLAlchemy(app)

#>>> from app/models import db
#>>> db.create_all()

@app.route("/")
def hello_world():
  return "Hello, World!"

