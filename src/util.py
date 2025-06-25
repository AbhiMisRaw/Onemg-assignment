import os
import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from .model import User as UserModel
from .schema import User

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY=os.getenv("SECRET_KEY","asdasdasd234sdf45dfgre5dfgacnhkjd3242fs234gee56d")
ALGORITHM=os.getenv("ALGORITHM","HS256")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
    user = get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user


def get_user_by_email(email:str, db: Session):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user:
        return user
    return None


def convert_user_model_to_schema(user: UserModel):
    user_schema = User(
        id=user.id,
        name=user.name,
        email=user.email,
        city=user.city,
        age=user.age
    )
    return user_schema