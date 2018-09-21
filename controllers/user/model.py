# coding: utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from utils.serializer import OutputMixin

db = SQLAlchemy()


class User(OutputMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    _hash = db.Column(db.Text, nullable=True)
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
        if name != 'created_at' and name != 'modified_at':
            super(User, self).__setattr__(name, value)
            super(User, self).__setattr__('modified_at', datetime.now())

    def _set_last_login(self):
        super(User, self).__setattr__('last_login', datetime.now())
        db.session.commit()

    def __repr__(self):
        return '<User %s>' % self.name
