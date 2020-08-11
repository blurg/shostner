from shostner.db.mongodb import get_database
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from ..models.users import UserIn, UserOut
import json
from datetime import datetime, timedelta
from hashlib import sha256
from typing import List, Optional
from ..utils import clean_ids_from_list
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..config import SECRET_KEY, ALGORITHM
from shostner.models.users import TokenData

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

#TODO: Use timezone aware datetime
async def get_user_by_username_with_password(db: AsyncIOMotorClient, username: str) -> UserOut:
    result = await db.user_collection.find_one({"name": username})
    if result is None:
        raise ValueError("No such user")
    result["id"] = str(result.pop("_id"))
    return UserIn(**result)

async def get_user_by_username(db: AsyncIOMotorClient, username: str) -> UserOut:
    result = await db.user_collection.find_one({"name": username})
    if result is None:
        raise ValueError("No such user")
    result["id"] = str(result.pop("_id"))
    return UserOut(**result)

async def create_user(db: AsyncIOMotorClient, user: UserIn) -> UserOut:
    user.created = datetime.now()
    user.password = pwd_context.hash(user.password.get_secret_value())
    result = await db.user_collection.insert_one( json.loads(user.json()))
    return await get_user(db, result.inserted_id)

async def fetch_all_users(db: AsyncIOMotorClient) -> List[UserOut]:
    result = await clean_ids_from_list(db.user_collection.find())
    result = [UserOut(**item) for item in result]
    return result 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return pwd_context.hash(password)

async def authenticate_user(db: AsyncIOMotorClient, username: str, password: str):
    user = await get_user_by_username_with_password(db, username)
    if not user:
        return False
    if not verify_password(password, user.password.get_secret_value()):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(db: AsyncIOMotorClient = Depends(get_database), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(token)
    try:
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserOut = Depends(get_current_user)):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user