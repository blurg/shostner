from typing import Optional
from pydantic import BaseModel, EmailStr, SecretStr
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
    created: datetime = None

    class Config:
        orm_mode = True

class UserIn(UserBase):
    password: SecretStr


class UserOut(UserBase):
    id: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None