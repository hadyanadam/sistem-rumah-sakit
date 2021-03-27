from pydantic import BaseModel
from datetime import datetime
from fastapi import Query

class Dokter(BaseModel):
  id: int
  nama: str
  alamat: str
  tempat_lahir: str
  tanggal_lahir: datetime
  no_hp: str
  poli: str
  created_at: datetime
  updated_at: datetime

class DokterCreate(Dokter):
  nama: str = Query(..., max_length=60)
  alamat: str = Query(..., max_length=130)
  tempat_lahir: str = Query(..., max_length=20)
  no_hp: str = Query(..., max_length= 15)