"""application.py."""

import sys
import logging
import time
from flask import Flask, request, url_for, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.contrib.fixers import ProxyFix
from flask_wtf.csrf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension
from six import iteritems

from utils.helpers import _import_submodules_from_package
from utils.account import get_current_user
import buildDB
import controllers

# convert python's encoding to utf8
try:
    from imp import reload

    reload(sys)
    sys.setdefaultencoding('utf8')
except (AttributeError, NameError):
    pass



def create_app(**config_overrides):
    """Short summary.

    Parameters
    ----------
    **config_overrides : type
        Description of parameter `**config_overrides`.

    Returns
    -------
    type
        Description of returned object.

    """
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile('settings.py')

    # apply overrides for tests
    app.config.update(config_overrides)

    # Proxy fix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # CSRF protect
    CsrfProtect(app)

    if app.debug or app.testing:
        DebugToolbarExtension(app)

        # Serve static files
        # app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        #     '/pages': os.path.join(app.config.get('PROJECT_PATH'), \
        # 'application/pages')
        # })
    else:
        # Log errors to stderr in production mode
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.ERROR)

        from raven.contrib.flask import Sentry
        sentry = Sentry()

        # Enable Sentry
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
    register_routes(app)
    register_db(app)
    register_error_handle(app)
    register_hooks(app)

    return app


def register_db(app):
    if not buildDB.setup_db():
        sys.exit()
    db = SQLAlchemy()
    db.init_app(app)

    from controllers.instance.model import Instance
    with app.test_request_context():
        db.create_all()
        db.session.commit()

    # migrate = Migrate(app, db)
    return app


def register_routes(app):
    """Register routes."""
    import controllers
    from flask.blueprints import Blueprint

    for module in _import_submodules_from_package(controllers):
        for submodule in _import_submodules_from_package(module):
            module_name = submodule.__name__.split('.')[-1]
            if module_name == 'routes':
                print("Loading routes : %s" % submodule.__name__)
                bp = getattr(submodule, 'bp')
                if bp and isinstance(bp, Blueprint):
                    app.register_blueprint(bp)


def register_error_handle(app):
    """Register HTTP error pages."""

    @app.errorhandler(403)
    def page_403(error):
        return render_template('site/403/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('site/404/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('site/500/500.html'), 500


def register_hooks(app):
    """Register hooks."""

    @app.before_request
    def before_request():
        g.user = get_current_user()
        if g.user and g.user.is_admin:
            g._before_request_time = time.time()

    @app.after_request
    def after_request(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g._before_request_time
            response.headers['X-Render-Time'] = delta * 1000
        return response


def _get_template_name(template_reference):
    """Get current template name."""
    return template_reference._TemplateReference__context.name
