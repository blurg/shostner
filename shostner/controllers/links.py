from shostner.models.links import Link, LinkOut
from motor.motor_asyncio import AsyncIOMotorClient

from datetime import datetime
from hashlib import sha256
from typing import List
from ..utils import clean_ids_from_list
from ..config import DEFAULT_URL

async def get_link_by_name(db: AsyncIOMotorClient, link_name: str) -> str:
    result = await db.link_collection.find_one({"name": link_name})
    if result is None:
        return DEFAULT_URL
    return result["url"]

async def get_link(db: AsyncIOMotorClient, link_id: str) -> LinkOut:
    result = await db.link_collection.find_one({"_id": link_id})
    if result is None:
        raise ValueError("No such Link")

    result["id"] = str(result.pop("_id"))

    return LinkOut(**result)

async def create_link(db: AsyncIOMotorClient, link: Link) -> LinkOut:
    link.created = datetime.now()
    result = await db.link_collection.insert_one( link.dict() )
    return await get_link(db, result.inserted_id)

async def fetch_all_links(db: AsyncIOMotorClient) -> List[LinkOut]:
    result = await clean_ids_from_list(db.link_collection.find())
    result = [LinkOut(**item) for item in result]
    return result 