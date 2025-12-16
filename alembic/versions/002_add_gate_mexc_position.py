"""Add gate_position and mexc_position columns

Revision ID: 002_add_positions
Revises: 001_initial
Create Date: 2025-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_positions'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add gate_position column to signals_funding_rate table
    op.add_column('signals_funding_rate', sa.Column('gate_position', sa.String(length=10), nullable=True))
    
    # Add mexc_position column to signals_funding_rate table
    op.add_column('signals_funding_rate', sa.Column('mexc_position', sa.String(length=10), nullable=True))


def downgrade() -> None:
    # Remove mexc_position column
    op.drop_column('signals_funding_rate', 'mexc_position')
    
    # Remove gate_position column
    op.drop_column('signals_funding_rate', 'gate_position')
