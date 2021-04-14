import random
from sqlalchemy.orm import Session
from .base_seeder import faker
from ..crud.crud_pasien import crud_pasien
from ..schemas.pasien import PasienCreate

def seed_pasien(iter, db):
  for i in range(iter):
    pasien = PasienCreate(
      nama=faker.name(),
      alamat=faker.address(),
      tanggal_lahir=faker.date(),
      tempat_lahir=faker.city()[:20],
      no_hp=faker.phone_number(),
      bpjs=faker.pybool(),
      rfid=str(faker.random_int(10)),
    )
    crud_pasien.create(
      db=db,
      obj_in=pasien
    )