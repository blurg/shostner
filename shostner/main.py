from fastapi import FastAPI, Header, Request, BackgroundTasks, Depends
from starlette.responses import RedirectResponse
from typing import Optional
from .db.mongodb import AsyncIOMotorClient, get_database
from .db.mongodb_utils import close_mongo_connection, connect_to_mongo



app = FastAPI()
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)
"""
url.jlugao.com/live10
-> slides


- Link + curto do que speackerdeck.com/fulano/xyz

- Analytics -> na live do edu eu recebi 50 acessos
            -> numa talk no grupy-sp eu recebi 20 acessos


"""

urls = {
    "google": "http://www.google.com.br",
    "jlugao": "http://jlugao.com"
}

def log_access_info(shortened_url: str, user_agent: str, referer: str, ip: str, language: str):
    print("Just Redirected a request with the following data")
    print(f"Shortened URL: {shortened_url}")
    print(f"Targer URL: {urls.get(shortened_url, 'http://www.facebook.com')}")
    print(f"User Agent: {user_agent}")
    print(f"Referer: {referer}")
    print(f"Ip: {ip}")
    print(f"Language Preferences: {language}")
    print("====================")


def id_to_str(value: dict) -> dict:
    value["id"] = str(value.pop("_id"))
    return value

@app.get("/urls")
async def list_urls(db: AsyncIOMotorClient = Depends(get_database)):
    """
    List Created Urls
    """
    cursor = db.url_collection.find()
    result = [id_to_str(doc) async for doc in cursor]
    return result

@app.post("/urls")
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


@app.get("/{shortened_url}")
async def get_url(  shortened_url: str, 
                    request: Request,  
                    background_tasks: BackgroundTasks,
                    user_agent: Optional[str] = Header(None), 
                    accept_language: Optional[str] = Header(None), 
                    referer: Optional[str] = Header(None)):

    background_tasks.add_task(log_access_info, shortened_url, user_agent, 
                                referer, request.client.host, accept_language)
    
    return RedirectResponse(url=urls.get(shortened_url, "http://www.facebook.com"))
