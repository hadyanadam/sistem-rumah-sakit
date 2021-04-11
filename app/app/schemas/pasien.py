from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from fastapi import Query

class Pasien(BaseModel):
  id: int
  nama: str
  alamat: str
  tempat_lahir: str
  tanggal_lahir: datetime
  no_hp: str
  bpjs: bool
  rfid: str

class PasienCreate(Pasien):
  nama: str = Query(..., max_length=60)
  alamat: str = Query(..., max_length=130)
  tempat_lahir: str = Query(..., max_length=20)
  no_hp: str = Query(..., max_length= 15)

class PasienUpdate(Pasien):
  nama: Optional[str] = Query(..., max_length=60)
  alamat: Optional[str] = Query(..., max_length=130)
  tempat_lahir: Optional[str] = Query(..., max_length=20)
  no_hp: Optional[str] = Query(..., max_length= 15)
  bpjs: Optional[bool]
  rfid: Optional[str]

class PasienRetrieve(Pasien):
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode=True