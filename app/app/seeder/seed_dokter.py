import random
from sqlalchemy.orm import Session
from .base_seeder import faker
from ..crud.crud_dokter import crud_dokter
from ..schemas.dokter import DokterCreate

poli = [
  'Poli Umum',
  'Poli Penyakit Dalam',
  'Poli Gigi',
  'Poli Kandungan',
  'Poli Anak'
]

def seed_dokter(iter, db):
  for i in range(iter):
    dokter = DokterCreate(
      username=faker.unique.email(),
      password='user1234',
      nama=faker.name(),
      alamat=faker.address(),
      tanggal_lahir=faker.date(),
      tempat_lahir=faker.city()[:20],
      no_hp=faker.phone_number(),
      poli=random.choice(poli)
    )
    crud_dokter.create(
      db=db,
      obj_in=dokter
    )