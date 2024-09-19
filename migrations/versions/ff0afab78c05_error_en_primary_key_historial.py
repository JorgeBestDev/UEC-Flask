"""error en primary key historial

Revision ID: ff0afab78c05
Revises: c397e82c8a9e
Create Date: 2024-09-11 10:41:55.318080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff0afab78c05'
down_revision: Union[str, None] = 'c397e82c8a9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('historial', sa.Column('idHistorial', sa.Integer(), autoincrement=True, nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('historial', 'idHistorial')
    # ### end Alembic commands ###
