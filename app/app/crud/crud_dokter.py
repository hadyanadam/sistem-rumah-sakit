from typing import Any, Dict, Optional, Union, List
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..core.crud_base import CRUDBase
from ..models.dokter import Dokter
from ..schemas.dokter import DokterCreate, DokterUpdate
from ..schemas.user import UserCreate
from .crud_user import crud_user

class CRUDDokter(CRUDBase[Dokter, DokterCreate, DokterUpdate]):
  def create(self, db: Session, *, obj_in: DokterCreate) -> Dokter:
      data = obj_in.dict(exclude_unset=True)
      user_data = UserCreate(
          username=data.pop('username'),
          password=data.pop('password')
      )
      user = crud_user.create(db=db, obj_in=user_data)
      db_obj = Dokter(
          user_id=user.id,
          **data
      )
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

  def update(
      self, db: Session, *, db_obj: Dokter, obj_in: Union[DokterUpdate, Dict[str, Any]]
  ) -> Dokter:
      if isinstance(obj_in, dict):
          update_data = obj_in
      return super().update(db, db_obj=db_obj, obj_in=update_data)

crud_dokter = CRUDDokter(Dokter)