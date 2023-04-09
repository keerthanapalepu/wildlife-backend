"""
Server app config
"""

# pylint: disable=import-error

from fastapi import FastAPI
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from myserver.config import CONFIG
from myserver.models.user import User


app = FastAPI()


@app.on_event("startup")
async def app_init():
    client = AsyncIOMotorClient(CONFIG.mongo_uri)
    await init_beanie(
        database=client["Wildlife"],
        document_models=[User],
    )