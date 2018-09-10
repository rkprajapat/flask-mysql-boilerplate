# coding: utf-8
from flask import Blueprint, redirect, request, url_for, Response, current_app
import json
from datetime import datetime
import traceback


from utils.permissions import AdminPermission
from controllers.instance.model import db, Instance
from utils.encoder_decoder import to_serializable


bp = Blueprint('instance', __name__)


@bp.route('/instances', methods=['GET'])
# @AdminPermission()
def list_all():
    try:
        result = Instance.query.all()
        if result:
            return Response(json.dumps([x.to_json() for x in result], default=to_serializable), status=200, mimetype='application/json')
        else:
            return Response(status=404)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return Response(status=404)


@bp.route('/instances/<int:instance_id>', methods=['GET'])
# @AdminPermission()
def list_one(instance_id):
    try:
        obj = Instance.query.get(instance_id)
        if obj:
            return Response(obj.to_json(), status=200, mimetype='application/json')
        else:
            return Response(status=404)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return Response(status=404)


@bp.route('/instances', methods=['POST'])
# @AdminPermission()
def create():
    try:
        data = request.get_json(silent=True)
        obj = Instance(**data)
        db.session.add(obj)
        db.session.commit()
        return Response(obj.to_json(), status=201, mimetype='application/json')
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        db.session.rollback()
        return Response(status=409)


@bp.route('/instances/<int:instance_id>', methods=['DELETE'])
# @AdminPermission()
def delete(instance_id):
    try:
        obj = Instance.query.get(instance_id)
        db.session.delete(obj)
        db.session.commit()
        return Response(status=200)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        db.session.rollback()
        return Response(status=404)


@bp.route('/instances/<int:instance_id>', methods=['PUT'])
# @AdminPermission()
def update(instance_id):
    try:
        obj = Instance.query.get(instance_id)
        data = request.get_json(silent=True)
        for key in data.keys():
            obj.__setattr__(key, data[key])
        db.session.commit()
        return Response(obj.to_json(), status=200, mimetype='application/json')
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        db.session.rollback()
        return Response(status=304)
