from motor.motor_asyncio import AsyncIOMotorClient
from ..models.users import UserIn, UserOut
import json
from datetime import datetime
from hashlib import sha256
from typing import List
from ..utils import clean_ids_from_list

#TODO: verify if passlib is needed
def validate_pass(user: UserIn, stored_hash: str):
    sha256(user.password.get_secret_value().encode("utf-8")).hexdigest() == stored_hash


#TODO: Use timezone aware datetime
async def get_user(db: AsyncIOMotorClient, user_id: str) -> UserOut:
    result = await db.user_collection.find_one({"_id": user_id})
    if result is None:
        raise ValueError("No such user")
    result["id"] = str(result.pop("_id"))
    return UserOut(**result)

async def create_user(db: AsyncIOMotorClient, user: UserIn) -> UserOut:
    user.created = datetime.now()
    user.password = sha256(user.password.get_secret_value().encode("utf-8")).hexdigest()
    result = await db.user_collection.insert_one( json.loads(user.json()))
    return await get_user(db, result.inserted_id)

async def fetch_all_users(db: AsyncIOMotorClient) -> List[UserOut]:
    result = await clean_ids_from_list(db.user_collection.find())
    result = [UserOut(**item) for item in result]
    return result 