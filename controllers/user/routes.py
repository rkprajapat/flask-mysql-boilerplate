# coding: utf-8
from flask import Blueprint, request, Response, current_app
import json
import traceback
from sqlalchemy import or_

from utils.permissions import AdminPermission
from controllers.user.model import db, User
from controllers.instance.model import Instance
from utils.encoder_decoder import to_serializable


bp = Blueprint('user', __name__)


@bp.route('/users', methods=['GET'])
# @AdminPermission()
def list_all():
    try:
        result = User.query.all()
        if result:
            return Response(json.dumps([x.to_json() for x in result],
                                       default=to_serializable),
                            status=200,
                            mimetype='application/json')
        else:
            return Response(status=404)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return Response(status=404)


@bp.route('/users/<int:instance_id>/<int:obj_id>', methods=['GET'])
# @AdminPermission()
def list_one(instance_id, obj_id):
    try:
        obj = User.query.filter(User.id == obj_id,
                                User.instance_id == instance_id).first()
        if obj:
            return Response(obj.to_json(),
                            status=200,
                            mimetype='application/json')
        else:
            return Response(status=404)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return Response(status=404)


@bp.route('/users', methods=['POST'])
# @AdminPermission()
def create():
    try:
        data = request.get_json(silent=True)
        obj = User(**data)
        db.session.add(obj)
        db.session.commit()
        return Response(obj.to_json(), status=201, mimetype='application/json')
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        db.session.rollback()
        return Response(status=409)


@bp.route('/users/<int:instance_id>/<int:obj_id>', methods=['DELETE'])
# @AdminPermission()
def delete(instance_id, obj_id):
    try:
        obj = User.query.filter_by(id=obj_id,
                                   instance_id=instance_id).first()
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return Response(status=200)
        else:
            return Response(status=404)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        db.session.rollback()
        return Response(status=404)


@bp.route('/users/<int:instance_id>/<int:obj_id>', methods=['PUT', 'PATCH'])
# @AdminPermission()
def update(instance_id, obj_id):
    try:
        obj = User.query.filter_by(id=obj_id,
                                   instance_id=instance_id).first()
        if obj:
            data = request.get_json(silent=True)
            for key in data.keys():
                obj.__setattr__(key, data[key])
            db.session.commit()
            return Response(obj.to_json(),
                            status=200,
                            mimetype='application/json')
        else:
            return Response(status=404)
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        db.session.rollback()
        return Response(status=304)
