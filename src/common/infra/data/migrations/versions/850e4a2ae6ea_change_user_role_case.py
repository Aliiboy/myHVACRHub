"""change user role case

Revision ID: 850e4a2ae6ea
Revises: 5cc1b5e7d596
Create Date: 2025-03-05 06:34:43.487890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '850e4a2ae6ea'
down_revision: Union[str, None] = '5cc1b5e7d596'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=False, 
                 server_default=sa.text("'2023-01-01 00:00:00'")))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_at')
    # ### end Alembic commands ###
