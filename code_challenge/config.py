"""Configuration for our Code Challenge"""


class CodeChallengeConfig:
    """Boilerplate and app specific parameters"""

    FLASK_DEBUG = True
    HOST = '0.0.0.0:5000'

    # Middleware
    SENTRY_POST_PATTERN = 'is_malicious'

    # Cache
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 2
