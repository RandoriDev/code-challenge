import json
import os
import time

import fastapi
from fastapi import Request

from services import request_inspector, crypto

router = fastapi.APIRouter()


@router.route('/', methods=['GET', 'POST', 'PUT'])
async def proxy_request(request: Request):
    response = ""
    if request.method == "POST":
        if await request_inspector.is_malicious(request):
            return fastapi.Response(
                content="Malicious request!", status_code=401
            )
    if request_inspector.is_duplicated(
        request.client.host, crypto.hash_request(request)
    ):
        response = await request_inspector.do_request(
            request, delay=os.getenv("DELAY_TIME")
        )
    else:
        response = await request_inspector.do_request(request) 

    return fastapi.Response(content=response, status_code=200)

