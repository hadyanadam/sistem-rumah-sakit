import sqlalchemy as sa
from app.db.base_class import Base

class User(Base):
  __tablename__ = 'users'

  id = sa.Column(sa.BigInteger, primary_key=True, index=True)
  nama = sa.Column(sa.String(60), nullable=False)
  alamat = sa.Column(sa.String(130), nullable=False)
  tempat_lahir = sa.Column(sa.String(20), nullable=False)
  tanggal_lahir = sa.Column(sa.DateTime(timezone=True), nullable=False)
  no_hp = sa.Column(sa.String(15), nullable=False)
  pengguna_bpjs = sa.Column(sa.Boolean, nullable=False)
  is_admin = sa.Column(sa.Boolean, nullable=False)

  created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
  updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __repr__(self):
    return f'<User {self.id}>'