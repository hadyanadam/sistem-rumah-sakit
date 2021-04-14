import random
from typing import List
from sqlalchemy.orm import Session
from .base_seeder import faker
from ..crud.crud_antrian import crud_antrian
from ..schemas.antrian import AntrianCreate

poli = [
  'Poli Umum',
  'Poli Penyakit Dalam',
  'Poli Gigi',
  'Poli Kandungan',
  'Poli Anak'
]

def seed_antrian(
  iter: int,
  db: Session,
  range_pasien_id: List[int],
):
  for i in range(iter):
    antrian = AntrianCreate(
      no_antrian=i+1,
      pasien_id=faker.random_int(min=range_pasien_id[0], max=range_pasien_id[1]),
      poli=random.choice(poli),
    )
    crud_antrian.create(
      db=db,
      obj_in=antrian
    )