# coding: utf-8
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Membership(db.Model):
    __tablename__ = 'group_memberships'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    instance_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def set_membership(self, user_id, group_id, instance_id):
        super(Membership, self).__setattr__('user_id', user_id)
        super(Membership, self).__setattr__('user_id', group_id)
        super(Membership, self).__setattr__('user_id', instance_id)

    def __repr__(self):
        return '<Membership %s>' % self.name
