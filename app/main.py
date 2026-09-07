import os
import platform

import psutil
import redis
from fastapi import FastAPI

app = FastAPI()
database = redis.Redis(
    host=os.environ["REDIS_HOST"],
    port=int(os.environ["REDIS_PORT"]),
    db=int(os.environ["REDIS_DB"]),
    password=os.environ["REDIS_PASSWORD"],
    decode_responses=True,
)


@app.get("/status")
async def status():
    return {
        "hostname": platform.node(),
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
    }


@app.post("/visit")
async def visit():
    return {"visits": database.incr("visits")}
