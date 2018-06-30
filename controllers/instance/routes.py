# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, Response
import json
from utils.permissions import AdminPermission
from controllers.instance.model import db, Instance
from utils.decorators import jsonify
from datetime import datetime

bp = Blueprint('instance', __name__)


@bp.route('/instances/<int:instance_id>', methods=['GET'])
# @AdminPermission()
def list(instance_id):
    print(instance_id)
    if instance_id:
        print('Checking instance for id', instance_id)
        result = Instance.query.get(1)
        print('Found result', result)
    else:
        result = Instance.query.all()
    print
    if result:

        return Response(json.dumps(result), status=200, mimetype='application/json')
    else:
        return Response('Instance not found', status=404)


@bp.route('/instances', methods=['POST'])
# @AdminPermission()
def create(data):
    return list_all()


@bp.route('/instances/<int:instance_id>', methods=['DELETE'])
# @AdminPermission()
def delete(instance_id):
    return list_all()


@bp.route('/instances/<int:instance_id>', methods=['PUT', 'PATCH'])
# @AdminPermission()
def update(instance_id, data):
    return list_all()
