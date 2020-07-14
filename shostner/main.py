from fastapi import FastAPI, Header, Request, BackgroundTasks
from starlette.responses import RedirectResponse
from typing import Optional

app = FastAPI()


urls = {
    "abc": "http://www.google.com.br"
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

@app.get("/{shortened_url}")
async def get_url(shortened_url: str, request: Request,  
                    background_tasks: BackgroundTasks,
                    user_agent: Optional[str] = Header(None), 
                    accept_language: Optional[str] = Header(None), 
                    referer: Optional[str] = Header(None)):
    background_tasks.add_task(log_access_info, shortened_url, user_agent, referer, request.client.host, accept_language)
    return RedirectResponse(url=urls.get(shortened_url, "http://www.facebook.com"))
