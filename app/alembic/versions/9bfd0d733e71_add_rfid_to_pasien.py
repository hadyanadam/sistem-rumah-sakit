"""add rfid to pasien

Revision ID: 9bfd0d733e71
Revises: f4b9e560530c
Create Date: 2021-04-08 13:45:53.894195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bfd0d733e71'
down_revision = 'f4b9e560530c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pasien', sa.Column('rfid', sa.String(length=60), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pasien', 'rfid')
    # ### end Alembic commands ###
