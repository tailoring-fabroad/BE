from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, HttpUrl

from src.app.schema import RWSchema
from src.authentication.models import User

class UserInLogin(RWSchema):
    email: EmailStr
    password: str

class UserInCreate(UserInLogin):
    username: str

class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image: Optional[HttpUrl] = None

class UserWithToken(User):
    token: str

class UserInResponse(RWSchema):
    user: UserWithToken

class JWTMeta(BaseModel):
    exp: datetime
    sub: str

class JWTUser(BaseModel):
    username: str