"""add genres and film_genre_association

Revision ID: 20250712_094557
Revises: bc76fdc50cbe
Create Date: 2025-07-12 09:45:57

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250712_094557'
down_revision = 'bc76fdc50cbe'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'genres',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
    )

    op.create_table(
        'film_genre_association',
        sa.Column('film_id', sa.Integer(), sa.ForeignKey('films_b2c.id', ondelete='CASCADE')),
        sa.Column('genre_id', sa.Integer(), sa.ForeignKey('genres.id', ondelete='CASCADE')),
    )

def downgrade():
    op.drop_table('film_genre_association')
    op.drop_table('genres')
