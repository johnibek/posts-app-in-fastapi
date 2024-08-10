"""add content column to posts table

Revision ID: 8f4993842038
Revises: 0b1b92a2d53b
Create Date: 2024-07-10 11:58:10.804108

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f4993842038'
down_revision: Union[str, None] = '0b1b92a2d53b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
