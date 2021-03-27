import sqlalchemy as sa
from app.db.base_class import Base
from .choice_type import ChoiceType

class Dokter(Base):
  __tablename__ = 'dokter'

  id = sa.Column(sa.BigInteger, primary_key=True, index=True)
  nama = sa.Column(sa.String(60), nullable=False)
  alamat = sa.Column(sa.String(130), nullable=False)
  tempat_lahir = sa.Column(sa.String(20), nullable=False)
  tanggal_lahir = sa.Column(sa.DateTime(timezone=True), nullable=False)
  no_hp = sa.Column(sa.String(15), nullable=False)
  poli = sa.Column(
    ChoiceType({
        'poli_anak': 'Poli Anak',
        'poli_kandungan': 'Poli Kandungan',
        'poli_gigi': 'Poli Gigi',
        'poli_umum': 'Poli Umum',
        'poli_penyakit_dalam': 'Poli Penyakit Dalam',
  }), nullable=False)

  created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
  updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __repr__(self):
    return f'<Dokter {self.id}>'

# 1. Dokter spesialis kandungan
# 2. Dokter spesialis anak
# 3. Dokter spesialis penyakit dalam
# 4. Dokter gigi
# 5. Dokter umum.