from typing import Any, Dict, Optional, Union, List
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..core.crud_base import CRUDBase
from ..models.pasien import Pasien
from ..schemas.pasien import PasienCreate, PasienUpdate

class CRUDPasien(CRUDBase[Pasien, PasienCreate, PasienUpdate]):
  def create(self, db: Session, *, obj_in: PasienCreate) -> Pasien:
      data = obj_in.dict(exclude_unset=True)
      db_obj = Pasien(
          **data
      )
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

  def update(
      self, db: Session, *, db_obj: Pasien, obj_in: Union[PasienUpdate, Dict[str, Any]]
  ) -> Pasien:
      if isinstance(obj_in, dict):
          update_data = obj_in
      return super().update(db, db_obj=db_obj, obj_in=update_data)

crud_pasien = CRUDPasien(Pasien)