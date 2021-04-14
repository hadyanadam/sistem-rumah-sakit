import sqlalchemy as sa
import datetime
from sqlalchemy.orm import relationship
from ..db.base_class import Base

class Dokter(Base):
  __tablename__ = 'dokter'

  id = sa.Column(sa.BigInteger, primary_key=True, index=True)
  user_id = sa.Column(sa.BigInteger, sa.ForeignKey('users.id'))
  nama = sa.Column(sa.String(60), nullable=False)
  alamat = sa.Column(sa.String(130), nullable=True)
  tempat_lahir = sa.Column(sa.String(20), nullable=True)
  tanggal_lahir = sa.Column(sa.DateTime(timezone=True), nullable=True)
  no_hp = sa.Column(sa.String(20), nullable=True)
  poli = sa.Column(sa.String(40), nullable=False)

  user = relationship('User', backref='dokter')

  created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
  updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __repr__(self):
    return f'<Dokter {self.id}>'

# 1. Dokter spesialis kandungan
# 2. Dokter spesialis anak
# 3. Dokter spesialis penyakit dalam
# 4. Dokter gigi
# 5. Dokter umum.