from fastapi import APIRouter, status, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from ..core.config import settings
from ..dependencies import get_db_session

from ..schemas.dokter import DokterCreate, DokterRetrieve, DokterUpdate
from ..models.user import User
from ..crud.crud_dokter import crud_dokter
from ..crud.crud_user import crud_user


router = APIRouter(prefix=f'{settings.API_V1_STR}/dokter')

@router.post(
  '/',
  status_code=status.HTTP_201_CREATED,
  response_model=DokterRetrieve,
  dependencies=[Depends(crud_user.get_current_user)]
)
async def create_dokter(input_data: DokterCreate, db: Session= Depends(get_db_session)):
  new_dokter = crud_dokter.create(obj_in=input_data, db=db)
  return new_dokter

@router.get('/', response_model=List[DokterRetrieve])
async def retrieve_dokter(db: Session= Depends(get_db_session), current_user: User = Depends(crud_user.get_current_user)):
  if current_user.is_admin:
    dokter = crud_dokter.get_multi(db=db)
    if len(dokter) == 0:
      raise HTTPException(status_code=status.HTTP_200_OK, detail="no data")
    return dokter
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.patch('/{id}', response_model=DokterRetrieve)
async def update_dokter(
  id: int,
  input_data: DokterUpdate,
  db: Session= Depends(get_db_session),
  current_user: User = Depends(crud_user.get_current_user)
):
  if current_user.is_admin:
    dokter = crud_dokter.get(id=id, db=db)
    return crud_dokter.update(db=db, db_obj=dokter, obj_in=input_data)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")