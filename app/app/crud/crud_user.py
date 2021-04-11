from typing import Any, Dict, Optional, Union, List
from fastapi import HTTPException, status, Depends, Cookie, Header
from sqlalchemy.orm import Session

from ..core.security import decode_jwt, credentials_exception
from ..core.security import get_password_hash, verify_password, oauth2_scheme, oauth2_scheme_login
from ..core.crud_base import CRUDBase
from ..dependencies import get_db_session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
  def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
      return db.query(User).filter(User.username == username).first()

  def create(self, db: Session, *, obj_in: UserCreate) -> User:
      data = obj_in.dict(exclude_unset=True)
      db_obj = User(
          password=get_password_hash(data.pop('password')),
          **data
      )
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj

  def update(
      self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
  ) -> User:
      if isinstance(obj_in, dict):
          update_data = obj_in
      else:
          update_data = obj_in.dict(exclude_unset=True)
      if update_data["password"]:
          hashed_password = get_password_hash(update_data["password"])
          update_data.update({"password": hashed_password})
      return super().update(db, db_obj=db_obj, obj_in=update_data)

  async def get_current_user(self, db: Session = Depends(get_db_session), token: str = Depends(oauth2_scheme)):
    token_data = await decode_jwt(token)
    user = self.get_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

  async def get_current_user_login(self, db: Session = Depends(get_db_session), access_token: str = Cookie(None)):
    print(access_token)
    if access_token is None:
        raise credentials_exception
    token_data = await decode_jwt(access_token)
    user = self.get_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

  def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
      user = self.get_by_username(db, username=username)
      if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
      if not verify_password(password, user.password):
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='password incorrect')
      return user

  def is_active(self, user: User) -> bool:
      return user.is_active

  def is_admin(self, user: User) -> bool:
      return user.is_admin

crud_user = CRUDUser(User)