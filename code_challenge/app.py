"""Assemble and present the WSGI App"""
import json
from logging.config import dictConfig
import logging

from flask import Flask, request
from flask_caching import Cache
from code_challenge.config import CodeChallengeConfig
from typing import Tuple

from .middleware.post_sentry import PostSentryMiddleware

LOGGER = logging.getLogger()


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] [%(levelname)s]: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app() -> Flask:
    """App factory, decouple dependencies to ease testing

    Returns:
        Flask app instance
    """
    app = Flask('code-challenge')
    app.config.from_object(CodeChallengeConfig)

    PostSentryMiddleware(app)

    add_routes(app)

    return app


def add_routes(app: Flask) -> None:
    """Separate routes to ease testing and reduce dependency coupling
    (in general, not much need here specifically)

    Args:
        app (Flask): Flask app instance

    Returns:
        None
    """
    cache = Cache(app)

    # Add our challenge 'backend'
    @app.route('/backend', methods=['POST'])
    @cache.memoize()
    def backend() -> Tuple[str, int, dict]:
        app.logger.info(f'Request passed to backend')
        return json.dumps({'success': True}), 200, {"Content-Type": "application/json"},
