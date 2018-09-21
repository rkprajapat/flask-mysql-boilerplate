"""application.py."""

import sys
import os
import logging
import logging.config
from datetime import datetime
from dateutil.relativedelta import relativedelta

import time
from flask import Flask, render_template, g, request, abort, session
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.wsgi import SharedDataMiddleware
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension

from utils.helpers import _import_submodules_from_package
# from utils.account import get_current_user
import buildDB
from logConfig import LoggerConfig
from flask.logging import default_handler

# convert python's encoding to utf8
try:
    from imp import reload

    reload(sys)
    sys.setdefaultencoding('utf8')
except (AttributeError, NameError):
    pass


def create_app(**config_overrides):
    app = Flask(__name__, template_folder='client')
    CORS(app)  # TODO: change this to restrict domain in production

    # Load config
    app.config.from_pyfile('settings.py')

    jwt = JWTManager(app)

    # apply overrides for tests
    app.config.update(config_overrides)

    # Proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # CSRF protect
    # # TODO: enable CSRFProtect
    # CSRFProtect(app)

    # 'always' (default), 'never',  'production', 'debug'
    app.config['LOGGER_HANDLER_POLICY'] = 'always'
    app.logger  # initialise logger
    logging.config.dictConfig(LoggerConfig.dictConfig)

    # Serve static files
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/client': os.path.join(os.path.dirname(__file__), 'client')
    })

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.debug = True

    if app.debug or app.testing:
        DebugToolbarExtension(app)

    else:
        from raven.contrib.flask import Sentry
        sentry = Sentry()

        # TODO: Enable Sentry
        if app.config.get('SENTRY_DSN'):
            sentry.init_app(app, dsn=app.config.get('SENTRY_DSN'))

        # Serve static files
        # app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        #     '/static': os.path.join(app.config.get('PROJECT_PATH'), \
        # 'output/static'),
        #     '/pkg': os.path.join(app.config.get('PROJECT_PATH'), \
        # 'output/pkg'),
        #     '/pages': os.path.join(app.config.get('PROJECT_PATH'), \
        # 'output/pages')
        # })

    # Register components
    with app.app_context():
        register_routes(app)
        register_db(app)
        register_error_handle(app)
        register_hooks(app)

    return app


def register_db(app):
    # Check if database is already setup or not
    app.logger.info('Checking database setup')
    if not buildDB.setup_db(app):
        sys.exit()
    db = SQLAlchemy()
    db.init_app(app)

    # migrate = Migrate(app, db)


def register_routes(app):
    """Register routes."""
    import controllers
    from flask.blueprints import Blueprint

    for module in _import_submodules_from_package(controllers):
        for submodule in _import_submodules_from_package(module):
            module_name = submodule.__name__.split('.')[-1]
            if module_name == 'routes':
                app.logger.debug("Loading routes : %s" % submodule.__name__)
                bp = getattr(submodule, 'bp')
                if bp and isinstance(bp, Blueprint):
                    app.register_blueprint(bp)


def register_error_handle(app):
    """Register HTTP error pages."""

    @app.errorhandler(403)
    def page_403(error):
        return render_template('403/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('404/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('500/500.html'), 500


def register_hooks(app):
    """Register hooks."""

    @app.before_request
    def before_request():
        g.user = '' #get_current_user()
        # if g.user and g.user.is_admin:
        g._before_request_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers[
                'X-Render-Time'] = str(round(delta * 1000, 3)) + ' milliseconds'
        return response


def _get_template_name(template_reference):
    """Get current template name."""
    return template_reference._TemplateReference__context.name
