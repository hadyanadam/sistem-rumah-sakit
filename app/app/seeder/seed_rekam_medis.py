import random
from typing import List
from sqlalchemy.orm import Session
from .base_seeder import faker
from ..crud.crud_rekam_medis import crud_rekam_medis
from ..schemas.rekam_medis import RekamMedisCreate

def seed_rekam_medis(iter: int, db: Session, range_pasien_id: List[int], range_dokter_id: List[int]):
  for i in range(iter):
    rekam_medis = RekamMedisCreate(
      pasien_id=faker.random_int(min=range_pasien_id[0], max=range_pasien_id[1]),
      dokter_id=faker.random_int(min=range_dokter_id[0], max=range_dokter_id[1]),
      keluhan=faker.text()[:130],
    )
    crud_rekam_medis.create(
      db=db,
      obj_in=rekam_medis
    )