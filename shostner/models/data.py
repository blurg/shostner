from pydantic import BaseModel
from datetime import datetime

class Log(BaseModel):
    shortened_url: str
    long_url: str
    user_agent: str = None
    referer: str = None
    ip: str = None
    language: str = None
    created: datetime = None