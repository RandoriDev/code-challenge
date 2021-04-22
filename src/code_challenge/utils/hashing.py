"""
Randori Code Challenge hashing utils module.
"""

from typing import Any

import hashlib


def hash_object(obj: Any) -> str:
    """This function returned a MD5 hashed string representation of the given object.

    :param obj: Object
    :return: Hashed string representation of the given object
    """

    # Unicode-objects must be encoded before hashing
    return hashlib.md5(str(obj).encode("utf-8")).hexdigest()
