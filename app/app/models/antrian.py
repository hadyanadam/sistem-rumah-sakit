import sqlalchemy as sa
from sqlalchemy.orm import relationship
from ..db.base_class import Base
import datetime

class Antrian(Base):
  __tablename__ = 'antrian'

  id = sa.Column(sa.BigInteger, primary_key=True, index=True)
  pasien_id = sa.Column(sa.BigInteger, sa.ForeignKey('pasien.id'))
  no_antrian = sa.Column(sa.Integer, nullable=False)
  poli = sa.Column(sa.String(60), nullable=False)
  aktif = sa.Column(sa.Boolean, default=True)

  created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
  updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __repr__(self):
    return f'<Antrian {self.id}>'