import datetime
from typing import Any, Dict, Optional, Union, List
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..core.crud_base import CRUDBase
from ..models.antrian import Antrian
from ..schemas.antrian import AntrianCreate, AntrianUpdate
from ..schemas.pasien import PasienUpdate
from .crud_pasien import crud_pasien

class CRUDAntrian(CRUDBase[Antrian, AntrianCreate, AntrianUpdate]):
  def get_by_poli(self, db:Session,*, limit: int = 100, skip: int = 0) -> List[Antrian]:
      antrian = db.query(self.model).filter(self.model.aktif).order_by(self.model.asc()).offset(skip).limit(limit).all()
      return antrian

  def get_by_antrian_aktif_per_poli(self, db: Session, *, poli: str, limit: int = 5, skip: int = 0) -> List[Antrian]:
      antrian = db.query(self.model).filter(self.model.aktif and self.model.poli == poli).order_by(self.model.no_antrian).limit(limit).offset(skip).all()
      return antrian

  def get_by_pasien_antrian_aktif(self, db: Session, *, pasien_id: int) -> Antrian:
      antrian = db.query(self.model).filter(self.model.pasien_id == pasien_id and self.model.aktif).first()
      return antrian

  def create(self, db: Session, *, obj_in: AntrianCreate) -> Antrian:
      kemarin = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
      last_antrian = db.query(self.model).filter(
        self.model.poli == obj_in.poli and self.model.created_at.replace(hour=0, minute=0, second=0, microsecond=0) != kemarin).order_by(self.model.created_at.desc()).first()
      if last_antrian:
        no_antrian = last_antrian.no_antrian + 1
      else:
        no_antrian = 1
      data = obj_in.dict(exclude_unset=True)
      db_obj = Antrian(
          no_antrian=no_antrian,
          **data
      )
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

  def update(
      self, db: Session, *, db_obj: Antrian, obj_in: Union[AntrianUpdate, Dict[str, Any]]
  ) -> Antrian:
      if isinstance(obj_in, dict):
          update_data = obj_in
      return super().update(db, db_obj=db_obj, obj_in=update_data)

crud_antrian = CRUDAntrian(Antrian)