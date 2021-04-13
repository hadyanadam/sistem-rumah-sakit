from sqlalchemy.orm import Session
from ..crud.crud_user import crud_user
from ..schemas.user import UserCreate
from ..core.config import settings
from . import base  # noqa: F401
from ..models.rfid_temporary import RFIDTemporary


def init_db(db: Session) -> None:

  user = crud_user.get_by_username(db=db, username=settings.FIRST_SUPERUSER)
  if not user:
    user_in = UserCreate(
        username=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_admin=True,
    )
    crud_user.create(db, obj_in=user_in)

  rfid_temporary = db.query(RFIDTemporary).filter(RFIDTemporary.id == 1).first()
  if not rfid_temporary:
    rfid = RFIDTemporary(
      rfid='12345789',
      aktif=False
    )
    db.add(rfid)
    db.commit()
    db.refresh(rfid)