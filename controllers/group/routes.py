# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, Response
import json
from utils.permissions import AdminPermission
from controllers.user.model import db, User
from utils.decorators import jsonify
from datetime import datetime

bp = Blueprint('user', __name__)


@bp.route('/users/<int:user_id>', methods=['GET'])
# @AdminPermission()
def list(user_id):
    users = User.query.all()
    # print(sample_instances)
    return Response(json.dumps(users), status=200, mimetype='application/json')


@bp.route('/users', methods=['POST'])
# @AdminPermission()
def create(data):
    return list_all()


@bp.route('/users/<int:user_id>', methods=['DELETE'])
# @AdminPermission()
def delete(user_id):
    return list_all()


@bp.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
# @AdminPermission()
def update(user_id, data):
    return list_all()
