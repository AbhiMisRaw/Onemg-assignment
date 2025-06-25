import os
import jwt
from typing import List, Annotated
from dotenv import load_dotenv

from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .schema import UserRegsiter, UserLogin, User, UserUpdate
from .db import get_db
from .service import (
    create_user, 
    login_user, 
    fetch_user_by_id,
    get_user_by_email,
    update_user_by_id,
    convert_user_model_to_schema
    )

router = APIRouter(tags=["Auth"])
profile = APIRouter(prefix="/profile", tags=["Profile"])

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY","asdasdasd234sdf45dfgre5dfgacnhkjd3242fs234gee56d")
ALGORITHM=os.getenv("ALGORITHM","HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/register")
def regsiter(user : UserRegsiter, db: Session = Depends(get_db)):
    """
    Helps to register a User.
    """
    try:
        registered_user = create_user(user, db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return registered_user


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate the user.
    """
    try:
        response = login_user(user, db)
    except HTTPException as e:
        raise e
    return response


@profile.get("/me")
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email(email, db)
    if user is None:
        raise credentials_exception
    return convert_user_model_to_schema(user)



@profile.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    get the user by id.
    """
    return fetch_user_by_id(user_id, db)

@profile.put("/{user_id}")
def update_user(user_id: int, user_update_model: UserUpdate,db:Session = Depends(get_db), user: User = Depends(get_current_user)):
    return update_user_by_id(user_id=user_id,user_update=user_update_model,db=db)
