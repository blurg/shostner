from fastapi import APIRouter, Header, Request, BackgroundTasks, Depends
from ..models.users import UserIn, UserOut
from ..controllers.users import create_user, fetch_all_users, get_user
from ..db.mongodb import AsyncIOMotorClient, get_database
from typing import List
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/", response_model = UserOut)
async def create_user_route(user: UserIn, 
                            db: AsyncIOMotorClient = Depends(get_database)):
    return await create_user(db, user)

@router.get("/", response_model = List[UserOut])
async def fetch_all_users_route(db: AsyncIOMotorClient = Depends(get_database)):
    return await fetch_all_users(db)

@router.get("/{user_id}", response_model = UserOut)
async def get_user_route(user_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    return await get_user(db, ObjectId(user_id))