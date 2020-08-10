from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime

class Link(BaseModel):
    name: str
    url: AnyHttpUrl
    created: datetime = None

class LinkOut(Link):
    id: str