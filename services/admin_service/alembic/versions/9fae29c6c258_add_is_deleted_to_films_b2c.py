"""add is_deleted to films_b2c

Revision ID: 9fae29c6c258
Revises: 
Create Date: 2025-07-24 17:40:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9fae29c6c258'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('films_b2c', sa.Column('is_deleted', sa.Boolean(), server_default=sa.text('FALSE'), nullable=False))


def downgrade():
    op.drop_column('films_b2c', 'is_deleted')
