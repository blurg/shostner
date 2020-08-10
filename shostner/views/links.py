from shostner.models.links import Link, LinkOut
from fastapi import APIRouter, Header, Request, BackgroundTasks, Depends
from ..tasks.access_logs import log_access_info
from starlette.responses import RedirectResponse
from typing import Optional, List
from ..main import urls
from ..db.mongodb import AsyncIOMotorClient, get_database
router = APIRouter()
from ..controllers.links import create_link, fetch_all_links, get_link_by_name


def id_to_str(value: dict) -> dict:
    value["id"] = str(value.pop("_id"))
    return value

@router.get("/urls", response_model=List[LinkOut])
async def list_urls(db: AsyncIOMotorClient = Depends(get_database)):
    """
    List Created Urls
    """
    return await fetch_all_links(db)

@router.post("/urls", response_model=LinkOut)
async def create_url(link: Link, db: AsyncIOMotorClient = Depends(get_database)):
    """
    Creates a shortened url with:
    - url_long
    - url_short
    """
    print("create_url")
    result = await create_link(db, link)
    return result


@router.get("/{shortened_url}")
async def get_url(  shortened_url: str, 
                    request: Request,  
                    background_tasks: BackgroundTasks,
                    user_agent: Optional[str] = Header(None), 
                    accept_language: Optional[str] = Header(None), 
                    referer: Optional[str] = Header(None),
                    db: AsyncIOMotorClient = Depends(get_database)):

    url = await get_link_by_name(db, shortened_url)
    background_tasks.add_task(log_access_info, shortened_url, url, user_agent, 
                                referer, request.client.host, accept_language, db)
    return RedirectResponse(url=url)
