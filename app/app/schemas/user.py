from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi import Query

class User(BaseModel):
  id: int
  username: str
  password: str
  is_active: bool
  is_admin: bool

class UserCreate(User):
  id: Optional[int]
  username: str = Query(..., max_length=20, min_length=5)
  password: str = Query(..., max_length=20, min_length=8)
  is_active: Optional[bool]
  is_admin: Optional[bool]

class UserUpdate(UserCreate):
  username: Optional[str] = Query(..., max_length=20, min_length=5)
  password: Optional[str] = Query(..., max_length=20, min_length=8)

class UserRetrieve(User):
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode=True