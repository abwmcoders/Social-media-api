"""add remaining column to table post

Revision ID: f3c068d642dd
Revises: c97382595642
Create Date: 2022-10-04 20:55:24.056347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f3c068d642dd'
down_revision = 'c97382595642'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'post', 
        sa.Column('published', sa.Boolean(), nullable=False, server_default ='True'),
        )
    op.add_column(
        'post', 
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        )
    pass


def downgrade() -> None:
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')
    pass
