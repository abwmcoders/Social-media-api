"""add foreign key to post table

Revision ID: c97382595642
Revises: 6749db0bab2c
Create Date: 2022-10-04 19:46:39.495256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c97382595642'
down_revision = '6749db0bab2c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post', sa.Column('owner_id', sa.Integer(),nullable=False,))
    op.create_foreign_key(
        'post_user_fkey', 
        source_table="post", 
        referent_table="users", 
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete='CASCADE',
        )
    pass


def downgrade():
    op.drop_constraint('post_user_fkey', table_name='post')
    op.drop_column('post', 'owner_id')
    pass
