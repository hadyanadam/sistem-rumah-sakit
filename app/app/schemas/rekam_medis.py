from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from fastapi import Query

class RekamMedis(BaseModel):
  id: int
  keluhan: str

class RekamMedisCreate(RekamMedis):
  id: Optional[int]
  pasien_id: int
  dokter_id: int
  keluhan: str = Query(..., max_length=150)

class RekamMedisUpdate(RekamMedis):
  id: Optional[int]
  keluhan: str = Query(..., max_length=150)

class RekamMedisRetrieve(RekamMedis):
  created_at: datetime
  updated_at: datetime

  class Config:
    orm_mode=True
    json_encoders = {
      datetime: lambda v: v.strftime("%d %B %Y"),
    }

  @classmethod
  @validator('tanggal_lahir', pre=True)
  def time_validate(cls, v):
    return datetime.fromisoformat(v)
