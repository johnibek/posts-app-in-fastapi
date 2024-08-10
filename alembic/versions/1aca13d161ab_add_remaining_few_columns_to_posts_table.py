"""add remaining few columns to posts table

Revision ID: 1aca13d161ab
Revises: 5509d57f1a63
Create Date: 2024-07-10 12:40:01.827611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1aca13d161ab'
down_revision: Union[str, None] = '5509d57f1a63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE'))
    op.add_column('posts',
                  sa.Column('created_at',
                            sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'),
                            nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
