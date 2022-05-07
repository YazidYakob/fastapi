"""add content column to post table

Revision ID: 57adcf624bf5
Revises: 6d3ce4466ee1
Create Date: 2022-05-07 21:45:08.818651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57adcf624bf5'
down_revision = '6d3ce4466ee1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
