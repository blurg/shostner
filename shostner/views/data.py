from shostner.db.mongodb import get_database
from shostner.controllers.data import fetch_all_logs
from shostner.models.data import Log
from typing import List
from fastapi import APIRouter, Header, Request, BackgroundTasks, Depends
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter()


@router.get("/", response_model=List[Log])
async def list_all_logs(db: AsyncIOMotorClient = Depends(get_database)):
    return await fetch_all_logs(db)