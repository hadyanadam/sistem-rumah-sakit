import sqlalchemy as sa
from sqlalchemy.orm import relationship
from ..db.base_class import Base
import datetime

class Pasien(Base):
  __tablename__ = 'pasien'

  id = sa.Column(sa.BigInteger, primary_key=True, index=True)
  nama = sa.Column(sa.String(30), nullable=False)
  alamat = sa.Column(sa.String(130), nullable=True)
  tempat_lahir = sa.Column(sa.String(30), nullable=True)
  tanggal_lahir = sa.Column(sa.Date, nullable=True)
  no_hp = sa.Column(sa.String(20), nullable=True)
  bpjs = sa.Column(sa.Boolean, nullable=False, default=False)
  rfid = sa.Column(sa.String(60), nullable=True)
  antrian = relationship('Antrian', backref='pasien')

  created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
  updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __repr__(self):
    return f'<Pasien {self.id}>'

  @property
  def antrian_aktif(self):
    return [antrian for antrian in self.antrian if antrian.aktif]