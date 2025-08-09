"""create payment_attempts

Revision ID: 20250809114403
Revises: 
Create Date: 2025-08-09 11:44:03

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250809114403'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'payment_attempts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False, index=True),
        sa.Column('plan_id', sa.String(), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('provider_payment_id', sa.String(), nullable=True),
        sa.Column('provider_session_id', sa.String(), nullable=True),
        sa.Column('payment_method_id', sa.String(), nullable=True),
        sa.Column('idempotence_key', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('pending','succeeded','failed','canceled', name='paymentstatus'), nullable=False, server_default='pending'),
        sa.Column('amount', sa.Numeric(10,2), nullable=True),
        sa.Column('currency', sa.String(), nullable=True),
        sa.Column('duration_days', sa.Integer(), nullable=False),
        sa.Column('capture_required', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_unique_constraint('uq_provider_payment', 'payment_attempts', ['provider','provider_payment_id'])

def downgrade() -> None:
    op.drop_constraint('uq_provider_payment', 'payment_attempts', type_='unique')
    op.drop_table('payment_attempts')
    op.execute("DROP TYPE IF EXISTS paymentstatus")
