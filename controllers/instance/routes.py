# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, Response
import json
from utils.permissions import AdminPermission
from controllers.instance.model import db, Instance
from utils.decorators import jsonify
from datetime import datetime

bp = Blueprint('instance', __name__)

sample_instances = [
    {
        'id': 1,
        'name': 'Instance1',
        'owner_name': 'owner1',
        'owner_email': 'email1',
    },
    {
        'id': 2,
        'name': 'Instance2',
        'owner_name': 'owner2',
        'owner_email': 'email2',
    },
]


@bp.route('/instances', methods=['GET', 'POST'])
# @AdminPermission()
def list_all():
    instances = Instance.query.all()
    # print(sample_instances)
    return Response(json.dumps(instances), status=200, mimetype='application/json')


@bp.route('/instance', methods=['POST'])
# @AdminPermission()
def create(data):
    return list_all()


@bp.route('/instance/:id', methods=['DELETE'])
# @AdminPermission()
def delete(id):
    return list_all()


@bp.route('/instance/:id', methods=['PUT', 'PATCH'])
# @AdminPermission()
def update(id, data):
    return list_all()
