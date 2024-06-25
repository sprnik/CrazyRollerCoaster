from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    is_adult = db.Column(db.Boolean, nullable=False)
    tickets = db.relationship('Ticket', backref='visitor', lazy=True, cascade="all, delete-orphan")
    visits = db.relationship('Visit', backref='visitor', lazy=True, cascade="all, delete-orphan")

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'), nullable=False)
    ticket_type = db.Column(db.String(20), nullable=False)
    is_adult = db.Column(db.Boolean, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)

class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    theme_group = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    visits = db.relationship('Visit', backref='attraction', lazy=True, cascade="all, delete-orphan")

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'), nullable=False)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attraction.id'), nullable=False)
    visit_start_time = db.Column(db.DateTime, nullable=False)
    visit_end_time = db.Column(db.DateTime, nullable=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
