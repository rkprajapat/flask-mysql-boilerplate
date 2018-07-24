# coding: utf-8
from flask import Blueprint, redirect, request, url_for, Response
import json
from datetime import datetime


from utils.permissions import AdminPermission
from controllers.instance.model import db, Instance
from utils.encoder_decoder import to_serializable


bp = Blueprint('instance', __name__)


@bp.route('/instances', methods=['GET'])
# @AdminPermission()
def list_all():
    result = Instance.query.all()
    if result:
        return Response(json.dumps([x.to_json() for x in result], default=to_serializable), status=200, mimetype='application/json')
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
