# coding: utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(20), nullable=False, unique=True)
    _hash = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    instance_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)

    def set_password(self, pw):
        super(User, self).__setattr__('_hash', generate_password_hash(pw))

    def check_password(self, pw):
        return check_password_hash(self._hash, pw)

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.admin

    def __setattr__(self, name, value):
        super(User, self).__setattr__(name, value)
        super(User, self).__setattr__('modified_at', datetime.now())

    def __repr__(self):
        return '<User %s>' % self.name
