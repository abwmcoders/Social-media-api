"""create users table

Revision ID: 6749db0bab2c
Revises: 869e52a290e5
Create Date: 2022-10-04 19:33:00.890844

"""
from cgitb import text
from time import timezone
from typing import Collection
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6749db0bab2c'
down_revision = '869e52a290e5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), nullable=False), 
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(),nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        )
    pass


def downgrade():
    op.drop_table('users')
    pass
