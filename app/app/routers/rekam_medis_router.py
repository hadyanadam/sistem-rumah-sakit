from fastapi import APIRouter, status, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from ..core.config import settings
from ..dependencies import get_db_session

from ..models.user import User
from ..schemas.rekam_medis import RekamMedisCreate, RekamMedisRetrieve, RekamMedisUpdate
from ..crud.crud_rekam_medis import crud_rekam_medis
from ..crud.crud_user import crud_user


router = APIRouter(prefix=f'{settings.API_V1_STR}/rekam-medis')

@router.post(
  '/',
  status_code=status.HTTP_201_CREATED,
  response_model=RekamMedisRetrieve,
  dependencies=[Depends(crud_user.get_current_user)]
)
async def create_rekam_medis(input_data: RekamMedisCreate, db: Session= Depends(get_db_session)):
  new_rekam_medis = crud_rekam_medis.create(obj_in=input_data, db=db)
  return new_rekam_medis

@router.get('/', response_model=List[RekamMedisRetrieve])
async def retrieve_rekam_medis(db: Session= Depends(get_db_session), current_user: User = Depends(crud_user.get_current_user)):
  if len(current_user.dokter) == 0 or current_user.is_admin:
    rekam_medis= crud_rekam_medis.get_multi(db=db)
    if len(rekam_medis) != 0:
      raise HTTPException(status_code=status.HTTP_200_OK, detail='no data')
    return rekam_medis
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.get('/{pasien_id}', response_model=List[RekamMedisRetrieve])
async def retrieve_rekam_medis(pasien_id: int, db: Session= Depends(get_db_session), current_user: User = Depends(crud_user.get_current_user)):
  print(current_user.dokter)
  if len(current_user.dokter) != 0 or current_user.is_admin:
    rekam_medis= crud_rekam_medis.get_by_pasien_id(db=db, pasien_id=pasien_id)
    if len(rekam_medis) == 0:
      raise HTTPException(status_code=status.HTTP_200_OK, detail='no data')
    return rekam_medis
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@router.patch('/{id}', response_model=RekamMedisRetrieve)
async def update_dokter(
  id: int,
  input_data: RekamMedisUpdate,
  db: Session= Depends(get_db_session),
  current_user: User = Depends(crud_user.get_current_user)
):
  if current_user.dokter_id is not None:
    rekam_medis = crud_rekam_medis.get(id=id, db=db)
    return crud_rekam_medis.update(db=db, db_obj=rekam_medis, obj_in=input_data)
  else:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")