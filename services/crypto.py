from hashlib import md5


def hash_request(request):
    return md5(str(request).encode('utf-8')).hexdigest()