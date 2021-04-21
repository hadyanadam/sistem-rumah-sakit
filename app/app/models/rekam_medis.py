import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
import datetime

from ..db.base_class import Base

class RekamMedis(Base):
  __tablename__ = 'rekam_medis'

  id = sa.Column(sa.BigInteger, primary_key=True, index=True)
  dokter_id = sa.Column(sa.BigInteger, sa.ForeignKey('dokter.id'))
  pasien_id = sa.Column(sa.BigInteger, sa.ForeignKey('pasien.id'))
  keluhan = sa.Column(sa.String(150), nullable=False)
  created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
  updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

  dokter = relationship('Dokter', backref=backref('rekam_medis', cascade='all,delete'))
  pasien = relationship('Pasien', backref=backref('rekam_medis', cascade='all,delete'))

  def __repr__(self):
    return f'<RekamMedis {self.id}>'