from flask import Flask,render_template,redirect,request
from flask_bootstrap import Bootstrap
from database import db
from views import User,Theme,Motivation,Portforio,Post,Feedback

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///motivation.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
  return "Hello, World!"


if __name__=="__main__":
  app.run(debug=True)


