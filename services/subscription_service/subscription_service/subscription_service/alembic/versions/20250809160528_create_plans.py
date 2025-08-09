from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250809160528_create_plans'
down_revision = '20250808_141339_init'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'plans',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('title', sa.String(length=128), nullable=False),
        sa.Column('description', sa.String(length=512), nullable=True),
        sa.Column('price', sa.Numeric(10,2), nullable=False),
        sa.Column('currency', sa.String(length=8), nullable=False),
        sa.Column('duration_days', sa.Integer(), nullable=False),
        sa.Column('is_recurring', sa.Boolean(), nullable=False, server_default=sa.text('true')),
    )

def downgrade() -> None:
    op.drop_table('plans')
