# coding: utf-8
from flask import Blueprint, redirect, request, url_for, Response
import json
from utils.permissions import AdminPermission
from controllers.instance.model import db, Instance
from utils.decorators import jsonify
from datetime import datetime

bp = Blueprint('instance', __name__)


@bp.route('/instances', methods=['GET'])
# @AdminPermission()
def list_all():
    print('getting all')
    result = Instance.query.all()
    if result:
        all = [x.to_json() for x in result]
        print(all)
        return Response(json.dumps(all), status=200, mimetype='application/json')
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
