import hashlib

# dict used for tracking duplicate requests.
# Depending on the scale of the application, this could be implemented in Redis
duplicate_request_cache = {}

# An alternate implementation of this is using Flask-Input validators
def is_malicious(request):
    """ Determines if this request is malicious

        if request contains the key is_malicious it is considered
        a malicious request

        Parameters
        ----------
        request : Request
            The request as received from the client

    """
    is_malicious = request.json.get("is_malicious", None)
    if (is_malicious != None):
        return "This is a malicious request"
    
    return None

def repeat_request(ip, payload) -> bool:
    """ Determines if the same request was made by same client
        
        Use ip, payload combination as unique identifier.
        A unique identifier like client id, session id could be a 
        better unique identifier instead of ip.

        Parameters
        ----------
        ip : str
            ip address of the caller
        payload : str
            Request payload
    """

    hash_object = hashlib.md5(payload)
    payload_hash = (hash_object.hexdigest())
    ret_value = False

    if (ip in duplicate_request_cache and duplicate_request_cache[ip] == payload_hash):
        ret_value = True

    duplicate_request_cache[ip] = payload_hash

    return ret_value