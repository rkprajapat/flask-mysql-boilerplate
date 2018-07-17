# coding: utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Entity(db.Model):
    __tablename__ = 'entities'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), unique=True, nullable=False)
    created_by_user = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    active = db.Column(db.Boolean, default=True)

    def __setattr__(self, name, value):
        super(Entity, self).__setattr__(name, value)
        super(Entity, self).__setattr__('modified_at', datetime.now())

    def is_active(self):
        return self.active

    def __repr__(self):
        return '<Entity %s>' % self.name
