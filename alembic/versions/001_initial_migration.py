"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2025-12-14 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Subscriptions table
    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('plan', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('start_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_subscriptions_user_id'), 'subscriptions', ['user_id'], unique=False)
    op.create_index(op.f('ix_subscriptions_status'), 'subscriptions', ['status'], unique=False)

    # User preferences table
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('theme', sa.String(length=20), nullable=True),
        sa.Column('font_size', sa.String(length=20), nullable=True),
        sa.Column('notifications_enabled', sa.Boolean(), nullable=True),
        sa.Column('email_notifications', sa.Boolean(), nullable=True),
        sa.Column('mexc_spot_futures_enabled', sa.Boolean(), nullable=True),
        sa.Column('mexc_spot_futures_min_spread', sa.String(length=10), nullable=True),
        sa.Column('mexc_spot_futures_sound', sa.Boolean(), nullable=True),
        sa.Column('mexc_spot_futures_browser_notif', sa.Boolean(), nullable=True),
        sa.Column('mexc_spot_futures_email_notif', sa.Boolean(), nullable=True),
        sa.Column('funding_rate_enabled', sa.Boolean(), nullable=True),
        sa.Column('funding_rate_min_profit', sa.String(length=10), nullable=True),
        sa.Column('funding_rate_sound', sa.Boolean(), nullable=True),
        sa.Column('funding_rate_browser_notif', sa.Boolean(), nullable=True),
        sa.Column('funding_rate_email_notif', sa.Boolean(), nullable=True),
        sa.Column('mexc_dex_enabled', sa.Boolean(), nullable=True),
        sa.Column('mexc_dex_min_spread', sa.String(length=10), nullable=True),
        sa.Column('mexc_dex_sound', sa.Boolean(), nullable=True),
        sa.Column('mexc_dex_browser_notif', sa.Boolean(), nullable=True),
        sa.Column('mexc_dex_email_notif', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_user_preferences_user_id'), 'user_preferences', ['user_id'], unique=True)

    # MEXC Spot & Futures signals table
    op.create_table(
        'signals_mexc_spot_futures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('coin_name', sa.String(length=100), nullable=False),
        sa.Column('position', sa.String(length=10), nullable=True),
        sa.Column('spread', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('mexc_spot_price', sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column('mexc_futures_price', sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column('spot_url', sa.String(length=500), nullable=True),
        sa.Column('futures_url', sa.String(length=500), nullable=True),
        sa.Column('deposit_enabled', sa.Boolean(), nullable=True),
        sa.Column('withdrawal_enabled', sa.Boolean(), nullable=True),
        sa.Column('dex_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_signals_mexc_spot_futures_coin_name'), 'signals_mexc_spot_futures', ['coin_name'], unique=False)
    op.create_index(op.f('ix_signals_mexc_spot_futures_created_at'), 'signals_mexc_spot_futures', ['created_at'], unique=False)

    # Funding Rate signals table
    op.create_table(
        'signals_funding_rate',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('coin_name', sa.String(length=100), nullable=False),
        sa.Column('hourly_profit', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('gate_rate', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('gate_url', sa.String(length=500), nullable=True),
        sa.Column('gate_interval', sa.String(length=10), nullable=True),
        sa.Column('binance_rate', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('binance_url', sa.String(length=500), nullable=True),
        sa.Column('binance_interval', sa.String(length=10), nullable=True),
        sa.Column('mexc_rate', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('mexc_url', sa.String(length=500), nullable=True),
        sa.Column('mexc_interval', sa.String(length=10), nullable=True),
        sa.Column('ourbit_rate', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('ourbit_url', sa.String(length=500), nullable=True),
        sa.Column('ourbit_interval', sa.String(length=10), nullable=True),
        sa.Column('bitget_rate', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('bitget_url', sa.String(length=500), nullable=True),
        sa.Column('bitget_interval', sa.String(length=10), nullable=True),
        sa.Column('bitget_position', sa.String(length=10), nullable=True),
        sa.Column('bybit_rate', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('bybit_url', sa.String(length=500), nullable=True),
        sa.Column('bybit_interval', sa.String(length=10), nullable=True),
        sa.Column('bybit_position', sa.String(length=10), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_signals_funding_rate_coin_name'), 'signals_funding_rate', ['coin_name'], unique=False)
    op.create_index(op.f('ix_signals_funding_rate_created_at'), 'signals_funding_rate', ['created_at'], unique=False)

    # MEXC & DEX signals table
    op.create_table(
        'signals_mexc_dex',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('coin_name', sa.String(length=100), nullable=False),
        sa.Column('spread_percent', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('mexc_price', sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column('mexc_url', sa.String(length=500), nullable=True),
        sa.Column('dex_price', sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column('dexscreener_url', sa.String(length=500), nullable=True),
        sa.Column('max_size_usd', sa.Numeric(precision=15, scale=2), nullable=True),
        sa.Column('deposit_enabled', sa.Boolean(), nullable=True),
        sa.Column('withdrawal_enabled', sa.Boolean(), nullable=True),
        sa.Column('deposit_url', sa.String(length=500), nullable=True),
        sa.Column('withdrawal_url', sa.String(length=500), nullable=True),
        sa.Column('token_contract', sa.String(length=100), nullable=True),
        sa.Column('token_chain', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_signals_mexc_dex_coin_name'), 'signals_mexc_dex', ['coin_name'], unique=False)
    op.create_index(op.f('ix_signals_mexc_dex_created_at'), 'signals_mexc_dex', ['created_at'], unique=False)

    # Notifications table
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('signal_type', sa.String(length=50), nullable=True),
        sa.Column('signal_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_user_id'), 'notifications', ['user_id'], unique=False)
    op.create_index(op.f('ix_notifications_created_at'), 'notifications', ['created_at'], unique=False)
    op.create_index(op.f('ix_notifications_is_read'), 'notifications', ['is_read'], unique=False)

    # CoinMarketCap data table
    op.create_table(
        'coinmarketcap_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('crypto_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('symbol', sa.String(length=20), nullable=True),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('price_usd', sa.Numeric(precision=20, scale=8), nullable=True),
        sa.Column('change_24h', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('change_7d', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('market_cap_usd', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('volume_24h_usd', sa.Numeric(precision=20, scale=2), nullable=True),
        sa.Column('market_cap_dominance', sa.Numeric(precision=10, scale=4), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('crypto_id')
    )
    op.create_index(op.f('ix_coinmarketcap_data_symbol'), 'coinmarketcap_data', ['symbol'], unique=False)
    op.create_index(op.f('ix_coinmarketcap_data_expires_at'), 'coinmarketcap_data', ['expires_at'], unique=False)

    # Audit logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=True),
        sa.Column('resource_type', sa.String(length=50), nullable=True),
        sa.Column('resource_id', sa.String(length=100), nullable=True),
        sa.Column('old_values', sa.Text(), nullable=True),
        sa.Column('new_values', sa.Text(), nullable=True),
        sa.Column('ip_address', sa.String(length=50), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)
    op.create_index('ix_audit_logs_resource', 'audit_logs', ['resource_type', 'resource_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_audit_logs_resource', table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_created_at'), table_name='audit_logs')
    op.drop_index(op.f('ix_audit_logs_user_id'), table_name='audit_logs')
    op.drop_table('audit_logs')
    op.drop_index(op.f('ix_coinmarketcap_data_expires_at'), table_name='coinmarketcap_data')
    op.drop_index(op.f('ix_coinmarketcap_data_symbol'), table_name='coinmarketcap_data')
    op.drop_table('coinmarketcap_data')
    op.drop_index(op.f('ix_notifications_is_read'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_created_at'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_user_id'), table_name='notifications')
    op.drop_table('notifications')
    op.drop_index(op.f('ix_signals_mexc_dex_created_at'), table_name='signals_mexc_dex')
    op.drop_index(op.f('ix_signals_mexc_dex_coin_name'), table_name='signals_mexc_dex')
    op.drop_table('signals_mexc_dex')
    op.drop_index(op.f('ix_signals_funding_rate_created_at'), table_name='signals_funding_rate')
    op.drop_index(op.f('ix_signals_funding_rate_coin_name'), table_name='signals_funding_rate')
    op.drop_table('signals_funding_rate')
    op.drop_index(op.f('ix_signals_mexc_spot_futures_created_at'), table_name='signals_mexc_spot_futures')
    op.drop_index(op.f('ix_signals_mexc_spot_futures_coin_name'), table_name='signals_mexc_spot_futures')
    op.drop_table('signals_mexc_spot_futures')
    op.drop_index(op.f('ix_user_preferences_user_id'), table_name='user_preferences')
    op.drop_table('user_preferences')
    op.drop_index(op.f('ix_subscriptions_status'), table_name='subscriptions')
    op.drop_index(op.f('ix_subscriptions_user_id'), table_name='subscriptions')
    op.drop_table('subscriptions')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')



