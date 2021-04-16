import sqlalchemy as sa
from sqlalchemy.orm import relationship
from ..db.base_class import Base
import datetime

class User(Base):
  __tablename__ = 'users'

  id = sa.Column(sa.BigInteger, primary_key=True, index=True)
  username = sa.Column(sa.String(50), unique=True, nullable=False)
  password = sa.Column(sa.String(60), nullable=False)
  is_active = sa.Column(sa.Boolean, default=True)
  is_admin = sa.Column(sa.Boolean, default=False)

  dokter = relationship('Dokter', backref='user')

  created_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
  updated_at = sa.Column(sa.DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

  def __repr__(self):
    return f'<User {self.id}>'