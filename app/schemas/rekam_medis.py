from pydantic import BaseModel
from datetime import datetime
from fastapi import Query

class RekamMedis(BaseModel):
  id: int
  keluhan: str
  created_at: datetime
  updated_at: datetime

class RekamMedisCreate(RekamMedis):
  keluhan: str = Query(..., max_length=150)