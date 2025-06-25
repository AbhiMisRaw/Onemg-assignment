from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserRegsiter(BaseModel):
    """
    Class for User Registration
    """
    name: str = Field(..., max_length=64)
    email: EmailStr
    password: str = Field(...,min_length=6)


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=0)
    city: Optional[str] = Field(default="")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    age: Optional[int] = Field(default=None, ge=0)
    city: Optional[str] = Field(default=None)
    

class UserLogin(BaseModel):
    """
    Class for User Login
    """
    email: EmailStr
    password: str