from fastapi import Request


__cache = {}

def get_request(client_address):
    return __cache.get(client_address, None)

def save_request(client_address, hashed_request):
    request_obj = {
        client_address: hashed_request
    }
    __cache.update(request_obj)
