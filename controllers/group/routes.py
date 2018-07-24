# coding: utf-8
from flask import render_template, Blueprint, redirect, request, url_for, Response
import json
from datetime import datetime


from utils.permissions import AdminPermission
from controllers.group.model import db, Group


bp = Blueprint('group', __name__)


@bp.route('/groups/<int:group_id>', methods=['GET'])
# @AdminPermission()
def list(group_id):
    groups = Group.query.all()
    # print(sample_instances)
    return Response(json.dumps(groups), status=200, mimetype='application/json')


@bp.route('/groups', methods=['POST'])
# @AdminPermission()
def create(data):
    return list_all()


@bp.route('/groups/<int:group_id>', methods=['DELETE'])
# @AdminPermission()
def delete(group_id):
    return list_all()


@bp.route('/groups/<int:group_id>', methods=['PUT', 'PATCH'])
# @AdminPermission()
def update(group_id, data):
    return list_all()
