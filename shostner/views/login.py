from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from shostner.models.users import Token, UserOut
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from shostner.controllers.users import (authenticate_user, 
                                        get_current_active_user,
                                        create_access_token)
from ..db.mongodb import AsyncIOMotorClient, get_database
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.get('/users/me', response_model=UserOut)
async def read_users_me(current_user: UserOut = Depends(get_current_active_user)):
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), 
                                    db: AsyncIOMotorClient = Depends(get_database)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

