from fastapi import APIRouter, status, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from ..dependencies import get_db_session
from ..core.config import settings

from ..models.user import User
from ..schemas.token import Token
from ..schemas.user import UserRetrieve, UserCreate
from ..core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from ..crud.crud_user import crud_user

router = APIRouter(
  prefix=f'{settings.API_V1_STR}/users',
  tags=['users'],
  # dependencies=[Depends(crud_user.get_current_user)]
)

@router.get('/me', response_model=UserRetrieve, dependencies=[])
async def retrieve_current_user(current_user: UserRetrieve = Depends(crud_user.get_current_user)):
  return current_user

@router.post("/token", response_model=Token, dependencies=[])
async def login_for_access_token(db: Session = Depends(get_db_session), form_data: OAuth2PasswordRequestForm = Depends()):
  user = crud_user.authenticate(db=db, username=form_data.username, password=form_data.password)
  if not user:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Incorrect username or password",
          headers={"WWW-Authenticate": "Bearer"},
      )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = await create_access_token(
      data={"sub": user.username}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "Bearer"}

@router.post(
  '/register',
  status_code=status.HTTP_201_CREATED,
  response_model=UserRetrieve,
  dependencies=[Depends(crud_user.get_current_user)]
)
async def create_user(input_user: UserCreate, db: Session= Depends(get_db_session)):
  if not crud_user.get_by_username(db=db, username=input_user.username):
    new_user = crud_user.create(obj_in=input_user, db=db)
    return new_user
  else:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exist")

@router.get('/', response_model=List[UserRetrieve])
async def retrieve_all_users(
  limit: int = 100,
  skip: int = 0,
  db: Session = Depends(get_db_session),
  current_user: UserRetrieve = Depends(crud_user.get_current_user)
):
  if not current_user.is_admin:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized User')
  return crud_user.get_multi(db=db, limit=limit, skip=skip)