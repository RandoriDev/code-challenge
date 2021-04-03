from time import sleep

import os

from fastapi import Request
import httpx
from httpx import Response

from infrastructure import ip_cache
from models.validation_error import ValidationError
from services.crypto import hash_request


async def is_malicious(request: Request):
    body = await request.json()
    if "isMalicious" in body:
        return True
    return False

def is_duplicated(client_address, hashed_request):
    last_request = ip_cache.get_request(client_address)
    if not last_request:
        return False
    if last_request == hashed_request:
        return True
    return False

async def do_request(request: Request, delay=None):
    if delay:
        sleep(delay)
    return await __do_request(request)

def save_request(request: Request):
    pass

async def __do_request(req: Request):
    backend_url = os.getenv("BACKEND_URL")
    backend_port = os.getenv("BACKEND_PORT")
    url = f"{backend_url}:{backend_port}"
    resp = None

    async with httpx.AsyncClient() as client:
        print(req.method)
        if req.method == "GET":

            resp: Response = await client.request(req.method, url)
        else:
            resp: Response = await client.request(req.method, url, data=req.body())
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)
    if resp:
        resp = resp.json()
    try:
        ip_cache.save_request(req, hash_request(req))
    except Exception as e:
        raise e

    return await resp