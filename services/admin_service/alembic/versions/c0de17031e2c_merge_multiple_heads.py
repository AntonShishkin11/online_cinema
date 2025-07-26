"""merge multiple heads

Revision ID: c0de17031e2c
Revises: 9fae29c6c258, e14f1af20612
Create Date: 2025-07-24 10:46:14.889410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0de17031e2c'
down_revision = ('9fae29c6c258', 'e14f1af20612')
branch_labels = None
depends_on = None

def upgrade():
    pass

def downgrade():
    pass
