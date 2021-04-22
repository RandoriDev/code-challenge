"""
Randori Code Challenge malicious utils module.
"""


def is_malicious(payload: dict) -> bool:
    """Determines whether the given payload is malicious.

    :param payload: Payload
    :return: Whether the given payload is malicious
    """

    if payload:
        value = payload.get("is_malicious", False)

        if isinstance(value, bool):
            return value

    return False
