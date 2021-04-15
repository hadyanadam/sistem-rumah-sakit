from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from fastapi import Query
from .rekam_medis import RekamMedisRetrieve
from .pasien import PasienRetrieve

class RekamMedisJoinPasien(RekamMedisRetrieve):
  pasien: List[PasienRetrieve]
