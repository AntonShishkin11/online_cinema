
from alembic import op
import sqlalchemy as sa
import enum

# revision identifiers, used by Alembic.
revision = "20250808_141339_init"
down_revision = None
branch_labels = None
depends_on = None

class SubscriptionStatus(sa.Enum):
    active = "active"
    inactive = "inactive"

def upgrade():
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), nullable=False, unique=True, index=True),
        sa.Column('status', sa.Enum('active', 'inactive', name='subscriptionstatus'), nullable=False, server_default='active'),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_subscriptions_user_status', 'subscriptions', ['user_id', 'status'])

def downgrade():
    op.drop_index('ix_subscriptions_user_status', table_name='subscriptions')
    op.drop_table('subscriptions')
