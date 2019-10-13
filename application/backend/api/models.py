from api import db

class User(db.Model):
    email_address = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean)

class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    author_difficulty = db.Column(db.Integer, nullable=False)
    viewer_difficulty = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    username = db.Column(db.String(80))

class Step(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(80), nullable=False)
    tutorial = db.Column(db.Integer)
    next = db.Column(db.Integer)
    previous = db.Column(db.Integer)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    edited = db.Column(db.Boolean)
    imaage = db.Column(db.String(120))

class List(db.Model):
    title = db.Column(db.String(20), primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    links = db.Column(db.String(120))
