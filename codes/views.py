from database import db


class User(db.Model):
    ___tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30),nullable=True)
    e_mail = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(30),nullable=False)
    profile_text = db.Column(db.String(500),default="profile_text")

    portforio = db.relationship('Portforio',backref='user')
    post = db.relationship('Post', backref='user')
    feedback = db.relationship('Feedback', backref='user')


class Theme(db.Model):
    __tablename__ = 'theme'
    id = db.Column(db.Integer, primary_key=True)
    theme_name = db.Column(db.String(100))


class Motivation(db.Model):
    __tablename__ = 'motivation'
    id = db.Column(db.Integer, primary_key=True)
    theme_name = db.Column(db.String(100))
    percentage = db.Column(db.Integer)
    due = db.Column(db.Date)
    valence = db.Column(db.Integer)
    instrumentary = db.Column(db.Integer)
    expectancy = db.Column(db.Integer)


class Portforio(db.Model):
    __tablename__ = 'portforio'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    portforio_title = db.Column(db.String(50), nullable=False)
    portforio_text = db.Column(db.String(500), nullable=False)
    portforio_img = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    post_title = db.Column(db.String(50), nullable=False)
    post_text = db.Column(db.String(500), nullable=False)
    post_img = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime)

    feedback = db.relationship('Feedback', backref='post', lazy=True)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'), nullable=False)
    feedback_text = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime)
