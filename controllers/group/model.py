# coding: utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Group(db.Model):
    __tablename__ = 'user_groups'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False, unique=True)
    instance_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    active = db.Column(db.Boolean, default=True)

    def __setattr__(self, name, value):
        super(Group, self).__setattr__(name, value)
        super(Group, self).__setattr__('modified_at', datetime.now())

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<Group %s>' % self.name
