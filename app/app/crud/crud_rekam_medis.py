from typing import Any, Dict, Optional, Union, List
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..core.crud_base import CRUDBase
from ..models.rekam_medis import RekamMedis
from ..schemas.rekam_medis import RekamMedisCreate, RekamMedisUpdate

class CRUDRekamMedis(CRUDBase[RekamMedis, RekamMedisCreate, RekamMedisUpdate]):
  def get_by_pasien_id(self, db: Session, *, pasien_id) -> List[RekamMedis]:
      rekam_medis = db.query(self.model).filter(self.model.pasien_id == pasien_id).all()
      return rekam_medis

  def create(self, db: Session, *, obj_in: RekamMedisCreate) -> RekamMedis:
      data = obj_in.dict(exclude_unset=True)
      db_obj = RekamMedis(
          **data
      )
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

  def update(
      self, db: Session, *, db_obj: RekamMedis, obj_in: Union[RekamMedisUpdate, Dict[str, Any]]
  ) -> RekamMedis:
      if isinstance(obj_in, dict):
          update_data = obj_in
      return super().update(db, db_obj=db_obj, obj_in=update_data)

crud_rekam_medis = CRUDRekamMedis(RekamMedis)