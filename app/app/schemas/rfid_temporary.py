from pydantic import BaseModel, validator
from typing import Optional, List
from fastapi import Query

class RFIDTemporary(BaseModel):
  id: int
  rfid: str
  aktif: bool

  class Config:
    orm_mode=True