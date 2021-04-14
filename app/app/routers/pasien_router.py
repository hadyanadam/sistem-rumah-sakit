from fastapi import APIRouter, status, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from ..core.config import settings
from ..dependencies import get_db_session

from ..schemas.pasien import PasienCreate, PasienRetrieve, PasienUpdate
from ..models.user import User
from ..crud.crud_pasien import crud_pasien
from ..crud.crud_user import crud_user


router = APIRouter(prefix=f'{settings.API_V1_STR}/pasien')

@router.post(
  '/',
  status_code=status.HTTP_201_CREATED,
  response_model=PasienRetrieve,
  dependencies=[Depends(crud_user.get_current_user)]
)
async def create_pasien(input_data: PasienCreate, db: Session= Depends(get_db_session)):
  new_pasien = crud_pasien.create(obj_in=input_data, db=db)
  return new_pasien

@router.get('/', response_model=List[PasienRetrieve])
async def retrieve_pasien(db: Session= Depends(get_db_session), current_user: User = Depends(crud_user.get_current_user)):
  if current_user.is_admin or current_user.dokter:
    pasien = crud_pasien.get_multi(db=db)
    if len(pasien) == 0:
      raise HTTPException(status_code=status.HTTP_200_OK, detail="no data")
    return pasien
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.patch('/{id}', response_model=PasienRetrieve)
async def update_pasien(
  id: int,
  input_data: PasienUpdate,
  db: Session= Depends(get_db_session),
  current_user: User = Depends(crud_user.get_current_user)
):
  if current_user.is_admin or current_user.dokter:
    pasien = crud_pasien.get(id=id, db=db)
    return crud_pasien.update(db=db, db_obj=pasien, obj_in=input_data)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")