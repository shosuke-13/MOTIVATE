from datetime import date
from sqlalchemy.orm import backref
from app import db

class User(db.Model):
    ___tablename__ = 'user'
    id = db.column(db.Integer, primary_key=True)
    username = db.column(db.text,nullable=True)
    e_mail = db.column(db.text,nullable=False)
    password = db.column(db.text,nullable=False)
    profile_text = db.column(db.text)

    motivation = db.relationship('Motivation', backref='user')
    theme = db.relationship('Theme', backref='user')
    portforio = db.relationship('Portforio',backref='user')
    post = db.relationship('Post', backref='user')
    feedback = db.relationship('Feedback', backref='user')

class Theme(db.Model):
    __tablename__ = 'theme'
    id = db.column(db.Integer, primary_key=True)
    user_id = db.column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    theme_name = db.column(db.Text)

    motivation = db.relationship('Motivation', backref='theme')
    portforio = db.relationship('Portforio',backref='theme')
    post = db.relationship('Post', backref='theme')


class Motivation(db.Model):
    __tablename__ = 'motivation'
    id = db.column(db.Integer, primary_key=True)
    user_id = db.column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    theme_id = db.column(db.Integer,db.ForeignKey('theme.id'), nullable=False)
    percentage = db.column(db.Integer)

class Portforio(db.Model):
    __tablename__ = 'portforio'
    id = db.column(db.Integer, primary_Key=True)
    user_id = db.column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    theme_id = db.column(db.Integer,db.ForeignKey('theme.id'), nullable=False)
    portforio_title = db.column(db.text)
    portforio_text = db.columun(db.text)
    date = db.column(db.datetime)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.column(db.Integer, primary_Key = True)
    user_id = db.column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    theme_id = db.column(db.Integer,db.ForeignKey('theme.id'), nullable=False)
    post_title = db.column(db.text)
    post_text = db.column(db.text)
    date = db.column(db.datetime)

    feedback = db.relationship('Feedback', backref='post', lazy=True)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.column(db.Integer, primary_Key = True)
    user_id = db.column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    post_id = db.column(db.Integer,db.ForeignKey('post.id'), nullable=False)
    feedback_text = db.column(db.Integer)
    date = db.column(db.datetime)


