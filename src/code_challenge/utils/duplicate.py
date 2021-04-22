"""
Randori Code Challenge duplicate utils module.
"""

# We will use a simple in-memory cache for this exercise. We could use a distributed cache or in-memory data grid
# solution if we needed a more feature-rich caching solution.
_cache = {}


def is_duplicate(client_host: str, request_hash: str) -> bool:
    """Determines whether the given request hash from the specific client is a duplicate.

    :param client_host: Client host
    :param request_hash: Hash of a request
    :return: Whether the given request hash from the client is a duplicate
    """

    # we are only checking the last recently received request
    return client_host in _cache and str.__eq__(request_hash, _cache.get(client_host))


def persist_request_hash(client_host: str, request_hash: str):
    """This function persists a given request hash from a specific client in the cache."""

    _cache[client_host] = request_hash
