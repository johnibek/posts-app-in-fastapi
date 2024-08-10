"""add foreign key to posts table

Revision ID: 5509d57f1a63
Revises: c2c94a40e7c4
Create Date: 2024-07-10 12:25:15.791563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5509d57f1a63'
down_revision: Union[str, None] = 'c2c94a40e7c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk',
                          source_table='posts',
                          referent_table='users',
                          local_cols=['user_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
