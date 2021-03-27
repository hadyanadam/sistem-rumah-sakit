from pydantic import BaseModel
from datetime import datetime
from fastapi import Query

class User(BaseModel):
  id: int
  nama: str
  alamat: str
  tempat_lahir: str
  tanggal_lahir: datetime
  no_hp: str
  pengguna_bpjs: bool
  is_admin: bool
  created_at: datetime
  updated_at: datetime

class UserCreate(User):
  nama: str = Query(..., max_length=60)
  alamat: str = Query(..., max_length=130)
  tempat_lahir: str = Query(..., max_length=20)
  no_hp: str = Query(..., max_length= 15)