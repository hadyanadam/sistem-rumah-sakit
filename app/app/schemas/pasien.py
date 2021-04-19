from pydantic import BaseModel, validator
from typing import Optional
from datetime import date, datetime
from fastapi import Query

class Pasien(BaseModel):
  id: int
  nama: str
  alamat: str
  tempat_lahir: str
  tanggal_lahir: date
  no_hp: str
  bpjs: bool
  rfid: str

class PasienCreate(Pasien):
  id: Optional[int]
  nama: str = Query(..., max_length=60)
  alamat: str = Query(..., max_length=130)
  tempat_lahir: str = Query(..., max_length=20)
  tanggal_lahir: str
  no_hp: str = Query(..., max_length= 20)
  class Config:
    json_encoders = {
      date: lambda v: f'{v.day}-{v.month}-{v.year}',
    }

  @classmethod
  @validator('tanggal_lahir', pre=True)
  def time_validate(cls, v):
    return date.fromisoformat(v)

class PasienUpdate(Pasien):
  id: Optional[int]
  nama: Optional[str] = Query(..., max_length=60)
  alamat: Optional[str] = Query(..., max_length=130)
  tempat_lahir: Optional[str] = Query(..., max_length=20)
  no_hp: Optional[str] = Query(..., max_length= 20)
  bpjs: Optional[bool]
  rfid: Optional[str]

class PasienRetrieve(Pasien):
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode=True

class PasienAntrian(Pasien):
  no_antrian: int
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode=True