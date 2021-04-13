import sqlalchemy as sa
from sqlalchemy.orm import relationship
from ..db.base_class import Base
import datetime

class RFIDTemporary(Base):
  __tablename__ = 'rfid_temporary'

  id = sa.Column(sa.BigInteger, primary_key=True, index=True)
  rfid = sa.Column(sa.String(60), unique=True, index=True)
  aktif = sa.Column(sa.Boolean, default=True)

  created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
  updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
