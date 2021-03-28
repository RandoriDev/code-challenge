import os

import fastapi
import uvicorn

from api import proxy


api = fastapi.FastAPI()

def configure():
    from dotenv import load_dotenv
    load_dotenv()
    configure_routing()

def configure_routing():
    api.include_router(proxy.router)

if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=os.getenv("PROXY_PORT"), host=os.getenv("PROXY_URL"))
else:
    configure()
