"""Validate request and payload"""

import json

from typing import TYPE_CHECKING

from werkzeug.wsgi import get_input_stream
from flask import Flask

if TYPE_CHECKING:
    from _typeshed.wsgi import WSGIEnvironment, StartResponse


class PostSentryMiddleware:
    """Inspect POST Body for disallowed content"""

    def __init__(self, app: Flask) -> None:
        """Set WSGI Callable with a post sentry

        Args:
            app (Flask): Flask app instance

        Returns:
            WSGIApplication
        """
        self.config = app.config
        wsgi_app = app.wsgi_app

        def sentry_wsgi_app(wsgi_environ: "WSGIEnvironment", start_response: "StartResponse"):
            post_body = self._read_post_body(wsgi_environ)
            if self._is_malicious(post_body):
                app.logger.error(f"Malicious content detected: {post_body}")
                start_response("401", [])
                return ""

            return wsgi_app(wsgi_environ, start_response)

        app.wsgi_app = sentry_wsgi_app

    @staticmethod
    def _read_post_body(wsgi_environ: "WSGIEnvironment") -> dict:
        """
        Args:
            wsgi_environ (WSGIEnvironment): Input environ

        Returns:
            Dictionary of Environ key/value pairs

        """
        return json.load(get_input_stream(wsgi_environ))

    def _is_malicious(self, post_body: dict) -> bool:
        """Check post body keys for 'is_malicious'

        Args:
            post_body (dict): dictionary containing contents of JSON post body

        Returns:
            Boolean: is this request malicious based on configured rulesets
        """
        # 1. Check for 'is_malicious' key within payload
        pattern = self.config.get('SENTRY_POST_PATTERN', 'is_malicious')
        if pattern in post_body:
            return True

        return False
