"""add binance and ourbit position columns

Revision ID: 003_add_binance_ourbit_position
Revises: 002_add_gate_mexc_position
Create Date: 2025-12-16
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "003_add_binance_ourbit_position"
down_revision = "002_add_gate_mexc_position"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "signals_funding_rate",
        sa.Column("binance_position", sa.String(length=10), nullable=True),
    )
    op.add_column(
        "signals_funding_rate",
        sa.Column("ourbit_position", sa.String(length=10), nullable=True),
    )


def downgrade():
    op.drop_column("signals_funding_rate", "ourbit_position")
    op.drop_column("signals_funding_rate", "binance_position")

