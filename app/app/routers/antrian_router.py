from fastapi import APIRouter, status, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from ..core.config import settings
from ..dependencies import get_db_session

from ..schemas.antrian import AntrianCreate, AntrianRetrieve, AntrianUpdate
from ..models.user import User
from ..crud.crud_antrian import crud_antrian
from ..crud.crud_user import crud_user


router = APIRouter(prefix=f'{settings.API_V1_STR}/antrian')

@router.post(
  '/',
  status_code=status.HTTP_201_CREATED,
  response_model=AntrianRetrieve,
)
async def create_antrian(input_data: AntrianCreate, db: Session= Depends(get_db_session)):
  new_antrian = crud_antrian.create(obj_in=input_data, db=db)
  return new_antrian

@router.get('/', response_model=List[AntrianRetrieve])
async def retrieve_antrian(db: Session= Depends(get_db_session), current_user: User = Depends(crud_user.get_current_user)):
  if current_user.is_admin:
    antrian = crud_antrian.get_multi(db=db)
    if len(antrian) == 0:
      raise HTTPException(status_code=status.HTTP_200_OK, detail='no data')
    return antrian
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.get('/poli', response_model=AntrianRetrieve)
async def antrian_poli(nama_poli: str, db: Session= Depends(get_db_session), current_user: User = Depends(crud_user.get_current_user)):
  if current_user.is_admin:
    return crud_antrian.get_by_poli(db=db, poli=nama_poli)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.get('/pasien/{pasien_id}', response_model=AntrianRetrieve)
async def antrian_single_pasien(pasien_id: int, db: Session= Depends(get_db_session), current_user: User = Depends(crud_user.get_current_user)):
  if current_user.is_admin:
    return crud_antrian.get_by_pasien_antrian_aktif(db=db, pasien_id=pasien_id)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.patch('/{id}', response_model=AntrianRetrieve)
async def update_antrian(
  id: int,
  input_data: AntrianUpdate,
  db: Session= Depends(get_db_session),
  current_user: User = Depends(crud_user.get_current_user)
):
  if current_user.is_admin:
    antrian = crud_antrian.get(id=id, db=db)
    return crud_antrian.update(db=db, db_obj=antrian, obj_in=input_data)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")