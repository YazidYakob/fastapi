"""add user table

Revision ID: e53d7d65bae3
Revises: 57adcf624bf5
Create Date: 2022-05-07 21:49:33.224475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e53d7d65bae3'
down_revision = '57adcf624bf5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('uid', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_on', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False))
    pass


def downgrade():
    op.drop_table('users')
    pass
