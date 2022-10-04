"""create post table

Revision ID: 872d0d0aafeb
Revises: 
Create Date: 2022-10-04 18:54:10.674865

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '872d0d0aafeb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'post', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
        sa.Column('title', sa.String(), nullable=False),
        )
    pass


def downgrade():
    op.drop_table('post')
    pass
