# Set the path
import os
import sys
import traceback
from flask import render_template, session, abort, request, redirect
import uuid

CSRF_TOKEN = '_csrf_token'

sys.setrecursionlimit(10000)
project_path = os.path.dirname(os.path.realpath(__file__))
if project_path not in sys.path:
    sys.path.append(project_path)

from application import create_app
app = create_app()


def generate_csrf_token():
    if CSRF_TOKEN not in session:
        session[CSRF_TOKEN] = str(uuid.uuid4())
    return session[CSRF_TOKEN]


@app.before_request
def csrf_protect():
    # # TODO: check CSRF protection
    pass
    # if request.method == "POST":
    #     token = session[CSRF_TOKEN]
    #     if not token or token != request.headers.get('X-XSRF-TOKEN'):
    #         abort(403)


@app.route('/', methods=['GET', 'POST'])
def redirect_ui_index_with_crsftoken():
    # response = app.make_response(redirect('src/index.html'))
    response = app.make_response('')
    response.set_cookie('XSRF-TOKEN', value=generate_csrf_token())
    return response
    # return render_template('src/index.html')


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        app.logger.error(e)
        # app.logger.error(traceback.format_exc())
