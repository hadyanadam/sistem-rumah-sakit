from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime, date
from fastapi import Query

class Antrian(BaseModel):
  id: int
  pasien_id: int
  no_antrian: int
  poli: str
  aktif: bool

class AntrianCreate(Antrian):
  id: Optional[int]
  pasien_id: Optional[int]
  poli: str = Query(..., max_length=60)
  aktif: bool = True

class AntrianUpdate(AntrianCreate):
  pasien_id: Optional[int]
  poli: Optional[str]
  aktif: Optional[bool]

class AntrianRetrieve(Antrian):
  created_at = datetime
  updated_at = datetime

  class Config:
    orm_mode=True