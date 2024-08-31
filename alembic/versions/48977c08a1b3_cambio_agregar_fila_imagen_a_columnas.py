"""Cambio agregar fila imagen a columnas 

Revision ID: 48977c08a1b3
Revises: 874897d5d732
Create Date: 2024-08-11 10:52:07.335964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48977c08a1b3'
down_revision: Union[str, None] = '874897d5d732'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reporte', sa.Column('imagen', sa.String(length=200), nullable=True))

    op.add_column('usuario', sa.Column('imagen', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuario', 'imagen')

    op.drop_column('reporte', 'imagen')
    # ### end Alembic commands ###