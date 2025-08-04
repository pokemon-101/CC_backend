from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class MusicAccountBase(BaseModel):
    platform: str
    platform_username: Optional[str] = None

class MusicAccountResponse(MusicAccountBase):
    id: int
    platform_user_id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class FriendshipRequest(BaseModel):
    friend_email: EmailStr

class FriendshipResponse(BaseModel):
    id: int
    friend_id: int
    friend_username: str
    friend_full_name: Optional[str] = None
    friend_avatar_url: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True