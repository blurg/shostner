from fastapi import APIRouter, Header, Request, BackgroundTasks, Depends
from ..tasks.access_logs import log_access_info
from starlette.responses import RedirectResponse
from typing import Optional
from ..main import urls
from ..db.mongodb import AsyncIOMotorClient, get_database
router = APIRouter()


@router.get("/{shortened_url}")
async def get_url(  shortened_url: str, 
                    request: Request,  
                    background_tasks: BackgroundTasks,
                    user_agent: Optional[str] = Header(None), 
                    accept_language: Optional[str] = Header(None), 
                    referer: Optional[str] = Header(None)):

    background_tasks.add_task(log_access_info, shortened_url, user_agent, 
                                referer, request.client.host, accept_language)
    
    return RedirectResponse(url=urls.get(shortened_url, "http://www.facebook.com"))


def id_to_str(value: dict) -> dict:
    value["id"] = str(value.pop("_id"))
    return value

@router.get("/urls")
async def list_urls(db: AsyncIOMotorClient = Depends(get_database)):
    """
    List Created Urls
    """
    cursor = db.url_collection.find()
    result = [id_to_str(doc) async for doc in cursor]
    return result

@router.post("/urls")
async def create_url(post_data: dict, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Creates a shortened url with:
    - url_long
    - url_short
    """
    url_long = post_data["url_long"]
    url_short = post_data["url_short"]
    result = await db.url_collection.insert_one({
        "url_long": url_long,
        "url_short": url_short
    })
    print(result)
    return {"id": repr(result.inserted_id)}
