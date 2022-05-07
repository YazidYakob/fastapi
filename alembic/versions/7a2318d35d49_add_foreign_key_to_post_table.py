"""add foreign-key to post table

Revision ID: 7a2318d35d49
Revises: e53d7d65bae3
Create Date: 2022-05-07 21:57:36.201712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a2318d35d49'
down_revision = 'e53d7d65bae3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('poster_user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', source_table="posts", referent_table="users",
                          local_cols=['poster_user_id'], remote_cols=['uid'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column('posts', 'poster_user_id')
    pass
