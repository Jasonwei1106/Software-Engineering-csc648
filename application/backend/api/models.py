from api import db

class User(db.Model):
    email_address = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean)

    # Relationships
    tutorials = db.relationship('Tutorial', backref='tutorial_owner')
    steps = db.relationship('Step', backref='user_step')

class Tutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    image = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    author_difficulty = db.Column(db.Integer, nullable=False)
    viewer_difficulty = db.Column(db.Integer)
    rating = db.Column(db.Integer)

    # ForeignKey
    username = db.Column(db.String(80), db.ForeignKey('user.username'))

    # Relationships
    steps = db.relationship('Step', backref='tutorial_steps')
    comments = db.relationship('Comment', backref='tutorial_comments')
    lists = db.relationship('List', backref='tutorial_lists')

class Step(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(80), nullable=False)

    # ForeignKey
    tutorial = db.Column(db.Integer, db.ForeignKey('tutorial.id'))
    user = db.Column(db.String(20), db.ForeignKey('user.username'))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    edited = db.Column(db.Boolean)
    imaage = db.Column(db.String(120))

    # ForeignKey
    tutorial = db.Column(db.Integer, db.ForeignKey('tutorial.id'))

class List(db.Model):
    title = db.Column(db.String(20), primary_key=True)
    content = db.Column(db.String(120), nullable=False)
    links = db.Column(db.String(120))

    # ForeignKey
    tutorial = db.Column(db.Integer, db.ForeignKey('tutorial.id'))
