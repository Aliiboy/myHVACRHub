"""role

Revision ID: 9facade2a863
Revises: 4b429ae7631d
Create Date: 2025-03-15 14:33:32.781346

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '9facade2a863'
down_revision: Union[str, None] = '4b429ae7631d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project_members_links', sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project_members_links', 'role')
    # ### end Alembic commands ###
