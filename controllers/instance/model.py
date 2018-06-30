# coding: utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Instance(db.Model):
    __tablename__ = 'instances'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    owner_name = db.Column(db.String(50), nullable=False)
    owner_email = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)

    def __setattr__(self, name, value):
        self.modified_at = datetime.now
        super(Instance, self).__setattr__(name, value)

    def __repr__(self):
        return '<Instance %s>' % self.name
