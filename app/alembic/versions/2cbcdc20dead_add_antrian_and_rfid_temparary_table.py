"""add antrian and rfid temparary table

Revision ID: 2cbcdc20dead
Revises: ce6d3398f894
Create Date: 2021-04-13 13:10:16.617331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cbcdc20dead'
down_revision = 'ce6d3398f894'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rfid_temporary',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('rfid', sa.String(length=60), nullable=True),
    sa.Column('aktif', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rfid_temporary_id'), 'rfid_temporary', ['id'], unique=False)
    op.create_index(op.f('ix_rfid_temporary_rfid'), 'rfid_temporary', ['rfid'], unique=True)
    op.create_table('antrian',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('pasien_id', sa.BigInteger(), nullable=True),
    sa.Column('no_antrian', sa.Integer(), nullable=False),
    sa.Column('poli', sa.String(length=60), nullable=False),
    sa.Column('aktif', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['pasien_id'], ['pasien.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_antrian_id'), 'antrian', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_antrian_id'), table_name='antrian')
    op.drop_table('antrian')
    op.drop_index(op.f('ix_rfid_temporary_rfid'), table_name='rfid_temporary')
    op.drop_index(op.f('ix_rfid_temporary_id'), table_name='rfid_temporary')
    op.drop_table('rfid_temporary')
    # ### end Alembic commands ###