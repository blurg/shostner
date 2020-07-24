import logging

from motor.motor_asyncio import AsyncIOMotorClient
from ..config import MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT
from .mongodb import db


async def connect_to_mongo():
    logging.info("Connecting to Mongo")
    db.client = AsyncIOMotorClient(str(MONGODB_URL), document_class=dict, 
                                   maxPoolSize=MAX_CONNECTIONS_COUNT,
                                   minPoolSize=MIN_CONNECTIONS_COUNT)
    logging.info("Mongo Db Connected!")


async def close_mongo_connection():
    logging.info("Closing Mongo Connection")
    db.client.close()
    logging.info("Mongo Connection Closed!")