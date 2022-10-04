"""add content column to post table

Revision ID: 869e52a290e5
Revises: 872d0d0aafeb
Create Date: 2022-10-04 19:25:23.648921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '869e52a290e5'
down_revision = '872d0d0aafeb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('post','content')
    pass
