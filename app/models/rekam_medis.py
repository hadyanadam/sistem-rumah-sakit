from sqlalchemy as sa
from sqlalchemy.orm import relationship
from datetime

from app.db.base_class import Base

class RekamMedis(Base):
  __tablename__ = 'rekam_medis'

  id = sa.Column(sa.BigInteger, primary_key=True, index=True)
  user_id = sa.Column(sa.BigInteger, sa.ForeignKey('users.id'))
  dokter_id = sa.Column(sa.BigInteger, sa.ForeignKey('dokter.id'))
  keluhan = sa.Column(sa.String(150), nullable=False)
  created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
  updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

  user = relationship('User', backref='rekam_medis')
  dokter = relationship('Dokter', backref='rekam_medis')

  def __repr__(self):
    return f'<RekamMedis {self.id}>'