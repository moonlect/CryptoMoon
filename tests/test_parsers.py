"""Tests for Telegram parsers."""
import pytest
from app.services.telegram.parsers import (
    MEXCSpotFuturesParser,
    FundingRateParser,
    MEXCDEXParser,
    detect_signal_type,
)


class TestMEXCSpotFuturesParser:
    """Tests for MEXC Spot & Futures parser."""

    def test_parse_valid_signal(self):
        """Test parsing valid MEXC Spot & Futures signal."""
        message = """Монета: NB
SHORT
Спред: 8.84%
https://www.mexc.com/exchange/NB_USDT
https://futures.mexc.com/exchange/NB_USDT
Спот: 0.00666400
Фючи: 0.00728000
Депозит: ✅ Вывод: ✅
https://dexscreener.com/bsc/0xc2bD425A63800731E3Ae42b6596BDD783299fCb1"""

        parser = MEXCSpotFuturesParser()
        result = parser.parse(message)

        assert result is not None
        assert result['coin_name'] == 'NB'
        assert result['position'] == 'SHORT'
        assert float(result['spread']) == 8.84
        assert float(result['mexc_spot_price']) == 0.00666400
        assert float(result['mexc_futures_price']) == 0.00728000
        assert result['deposit_enabled'] is True
        assert result['withdrawal_enabled'] is True

    def test_parse_invalid_signal(self):
        """Test parsing invalid signal."""
        message = "This is not a signal"
        parser = MEXCSpotFuturesParser()
        result = parser.parse(message)
        assert result is None

    def test_parse_missing_coin_name(self):
        """Test parsing signal without coin name."""
        message = "Спред: 8.84%"
        parser = MEXCSpotFuturesParser()
        result = parser.parse(message)
        assert result is None


class TestFundingRateParser:
    """Tests for Funding Rate parser."""

    def test_parse_valid_signal(self):
        """Test parsing valid Funding Rate signal."""
        message = """⚠️ PIPPIN Профит за час: 0.2711%
GATE (https://www.gate.com/uk/futures/USDT/PIPPIN_USDT): -0.0422% (интервал: 1.0h) 
BINANCE (https://www.binance.com/en/futures/PIPPINUSDT): -0.0258% (интервал: 1h) 
MEXC (https://futures.mexc.com/exchange/PIPPIN_USDT): -0.0267% (интервал: 1h) 
BYBIT (https://www.bybit.com/trade/usdt/PIPPINUSDT): -0.2698% (интервал: 1h) (LONG)"""

        parser = FundingRateParser()
        result = parser.parse(message)

        assert result is not None
        assert result['coin_name'] == 'PIPPIN'
        assert float(result['hourly_profit']) == 0.2711
        assert float(result['gate_rate']) == -0.0422
        assert float(result['binance_rate']) == -0.0258
        assert result['binance_position'] is None
        assert result['bybit_position'] == 'LONG'

    def test_parse_invalid_signal(self):
        """Test parsing invalid signal."""
        message = "This is not a funding rate signal"
        parser = FundingRateParser()
        result = parser.parse(message)
        assert result is None


class TestMEXCDEXParser:
    """Tests for MEXC & DEX parser."""

    def test_parse_valid_signal(self):
        """Test parsing valid MEXC & DEX signal."""
        message = """🔴 YEE 13.9%

Price Mxc (https://futures.mexc.com/exchange/YEE_USDT?inviteCode=1E5e4): 0.0221
Price Dexscreener (https://dexscreener.com/ethereum/0x9Ac9468E7E3E1D194080827226B45d0B892C77Fd): 0.0190

Max size | Deposit Withdrawal
 66$ | ✅ ✅

ETH: 0x9Ac9468E7E3E1D194080827226B45d0B892C77Fd"""

        parser = MEXCDEXParser()
        result = parser.parse(message)

        assert result is not None
        assert result['coin_name'] == 'YEE'
        assert float(result['spread_percent']) == 13.9
        assert float(result['mexc_price']) == 0.0221
        assert float(result['dex_price']) == 0.0190
        assert float(result['max_size_usd']) == 66
        assert result['deposit_enabled'] is True
        assert result['withdrawal_enabled'] is True
        assert result['token_chain'] == 'ETH'

    def test_parse_invalid_signal(self):
        """Test parsing invalid signal."""
        message = "This is not a MEXC & DEX signal"
        parser = MEXCDEXParser()
        result = parser.parse(message)
        assert result is None


class TestSignalTypeDetection:
    """Tests for signal type detection."""

    def test_detect_mexc_spot_futures(self):
        """Test detecting MEXC Spot & Futures signal."""
        message = "Монета: BTC\nСпред: 5%"
        signal_type = detect_signal_type(message)
        assert signal_type == 'mexc_spot_futures'

    def test_detect_funding_rate(self):
        """Test detecting Funding Rate signal."""
        message = "⚠️ BTC Профит за час: 0.5%"
        signal_type = detect_signal_type(message)
        assert signal_type == 'funding_rate'

    def test_detect_mexc_dex(self):
        """Test detecting MEXC & DEX signal."""
        message = "🔴 BTC 10%\nPrice Mxc: 50000"
        signal_type = detect_signal_type(message)
        assert signal_type == 'mexc_dex'

    def test_detect_unknown(self):
        """Test detecting unknown signal type."""
        message = "This is not a signal"
        signal_type = detect_signal_type(message)
        assert signal_type is None



