from pydantic import BaseModel, validator
from typing import Optional, Dict, Any
from datetime import datetime, date
from fastapi import Query, Form

class Dokter(BaseModel):
  id: int
  user_id: int
  nama: str
  alamat: str
  tempat_lahir: str
  tanggal_lahir: date
  no_hp: str
  poli: str

class DokterCreate(Dokter):
  id: Optional[int]
  user_id: Optional[int]
  username: str = Query(..., max_length=50)
  password: str = Query(..., max_length=20, min_length=8)
  nama: str = Query(..., max_length=60)
  alamat: str = Query(..., max_length=130)
  tanggal_lahir: str
  tempat_lahir: str = Query(..., max_length=20)
  no_hp: str = Query(..., max_length= 20)

  class Config:
    json_encoders = {
      date: lambda v: f'{v.day}-{v.month}-{v.year}',
    }

  @classmethod
  @validator('tanggal_lahir', pre=True)
  def time_validate(cls, v):
    return date.fromisoformat(v)


class DokterUpdate(DokterCreate):
  username: Optional[str]
  password: Optional[str]
  user_id: Optional[int]
  nama: Optional[str] = Query(..., max_length=60)
  alamat: Optional[str] = Query(..., max_length=130)
  tanggal_lahir: Optional[str]
  tempat_lahir: Optional[str] = Query(..., max_length=20)
  no_hp: Optional[str] = Query(..., max_length= 20)
  poli: Optional[str]

class DokterRetrieve(Dokter):
  user: Any
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode=True

class DokterFormUpdate(BaseModel):
  nama: Optional[str] = Form(...),
  email: Optional[str] = Form(...),
  alamat: Optional[str] = Form(...),
  no_hp: Optional[str] =Form(...),
  tempat_lahir: Optional[str] = Form(...),
  tanggal_lahir: Optional[str] = Form(...),
  poli: Optional[str] = Form(...),
  aktif: Optional[bool] = Form(...),