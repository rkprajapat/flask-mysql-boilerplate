# coding: utf-8
from flask import Blueprint, request, jsonify, current_app, Response
from datetime import datetime
import json
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
import traceback

from controllers.user.model import db, User
from utils.encoder_decoder import to_serializable

bp = Blueprint('account', __name__)


# With JWT_COOKIE_CSRF_PROTECT set to True, set_access_cookies() and
# set_refresh_cookies() will now also set the non-httponly CSRF cookies
# as well
@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json(silent=True)
        email = data['email']
        password = data['password']

        current_user = User.query.filter(User.email == email).first()
        if not current_user:
            return jsonify({'msg': 'Not a valid user'}), 401
        else:
            if not current_user.check_password(password) \
                    and not current_user.active:
                return jsonify({'msg': 'Email or Password did not match'}), 401
            else:
                # set last login time for user
                current_user._set_last_login()
                obj = json.loads(current_user.to_json())
                obj.pop('_hash', None)
                # Create the tokens we will be sending back to the user
                access_token = create_access_token(identity=email)
                refresh_token = create_refresh_token(identity=email)
                obj['token'] = access_token
                obj['refresh_token'] = refresh_token

        # # Set the JWTs and the CSRF double submit protection cookies
        # # in this response
        resp = jsonify(obj)
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp, 200
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
        return Response(status=401)


@bp.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the access JWT and CSRF double submit protection cookies
    # in this response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200


# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.
@bp.route('/logout', methods=['GET'])
def logout():
    print('logging out')
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
