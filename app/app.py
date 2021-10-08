from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from s19.app.models import Feedback, Motivation, Portforio, Post,Theme, User


app = Flask(__name__)
bootstrap = Bootstrap(app)
admin = Admin(app)

admin.add_view(ModelView(User,Motivation,Theme,Post,Portforio,Feedback))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motivation.db'
db = SQLAlchemy(app)

#>>> from app/models import db
#>>> db.create_all()

@app.route("/")
def hello_world():
  return "Hello, World!"

@app.route("/motivation", methods = ["GET", "POST"])
def motivation():
  if request.methods == "GET":
    themes = db.session.all(Theme)
    motivations = db.session.all(Motivation)
    return render_template("motivation.html", motivations= motivations,themes = themes)

  else:
    theme = request.form.get("theme")
    motivation = request.form.get("motivation")

    db.session.add(theme=theme)
    db.session.add(motivation=motivation)
    db.session.commit()

    return redirect("/")
