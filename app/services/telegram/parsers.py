"""Telegram message parsers for different signal types."""
import re
from typing import Optional, Dict, Any
from decimal import Decimal, InvalidOperation
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class SignalParser:
    """Base parser for Telegram signals."""

    @staticmethod
    def extract_urls(text: str) -> list[str]:
        """Extract all URLs from text."""
        url_pattern = r'https?://[^\s]+'
        return re.findall(url_pattern, text)

    @staticmethod
    def parse_boolean_flag(text: str, flag: str) -> bool:
        """Parse boolean flag like '✅ Депозит' or '❌ Вывод'."""
        pattern = rf'{flag}:\s*([✅❌])'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1) == '✅'
        return False


class MEXCSpotFuturesParser(SignalParser):
    """Parser for MEXC Spot & Futures signals."""

    @staticmethod
    def parse(message_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse MEXC Spot & Futures signal from Telegram message.
        
        Format:
        Монета: NB
        SHORT
        Спред: 8.84%
        https://www.mexc.com/exchange/NB_USDT
        https://futures.mexc.com/exchange/NB_USDT
        Спот: 0.00666400
        Фючи: 0.00728000
        Депозит: ✅ Вывод: ✅
        https://dexscreener.com/bsc/0xc2bD425A63800731E3Ae42b6596BDD783299fCb1
        """
        try:
            lines = message_text.split('\n')
            data = {}

            # Parse coin name
            coin_match = re.search(r'Монета:\s*(\w+)', message_text, re.IGNORECASE)
            if coin_match:
                data['coin_name'] = coin_match.group(1).strip()

            # Parse position (LONG/SHORT)
            if re.search(r'\bSHORT\b', message_text, re.IGNORECASE):
                data['position'] = 'SHORT'
            elif re.search(r'\bLONG\b', message_text, re.IGNORECASE):
                data['position'] = 'LONG'

            # Parse spread
            spread_match = re.search(r'Спред:\s*([\d.]+)%', message_text, re.IGNORECASE)
            if spread_match:
                data['spread'] = Decimal(spread_match.group(1))

            # Parse prices
            spot_match = re.search(r'Спот:\s*([\d.]+)', message_text, re.IGNORECASE)
            if spot_match:
                data['mexc_spot_price'] = Decimal(spot_match.group(1))

            futures_match = re.search(r'Фючи:\s*([\d.]+)', message_text, re.IGNORECASE)
            if futures_match:
                data['mexc_futures_price'] = Decimal(futures_match.group(1))

            # Extract URLs
            urls = SignalParser.extract_urls(message_text)
            for url in urls:
                if 'mexc.com/exchange' in url and 'futures' not in url:
                    data['spot_url'] = url
                elif 'futures.mexc.com' in url:
                    data['futures_url'] = url
                elif 'dexscreener.com' in url:
                    data['dex_url'] = url

            # Parse deposit/withdrawal flags
            deposit_match = re.search(r'Депозит:\s*([✅❌])', message_text)
            if deposit_match:
                data['deposit_enabled'] = deposit_match.group(1) == '✅'

            withdrawal_match = re.search(r'Вывод:\s*([✅❌])', message_text)
            if withdrawal_match:
                data['withdrawal_enabled'] = withdrawal_match.group(1) == '✅'

            # Validate required fields
            if not data.get('coin_name'):
                return None

            return data

        except (ValueError, InvalidOperation, AttributeError) as e:
            logger.warning("Error parsing MEXC Spot & Futures signal", error=str(e), message_preview=message_text[:100])
            return None
        except Exception as e:
            logger.error("Unexpected error parsing MEXC Spot & Futures signal", error=str(e), exc_info=True)
            return None


class FundingRateParser(SignalParser):
    """Parser for Funding Rate Spread signals."""

    @staticmethod
    def parse(message_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse Funding Rate signal from Telegram message.
        
        Format:
        ⚠️ PIPPIN Профит за час: 0.2711%
        GATE (https://www.gate.com/uk/futures/USDT/PIPPIN_USDT): -0.0422% (интервал: 1.0h) 
        BINANCE (https://www.binance.com/en/futures/PIPPINUSDT): -0.0258% (интервал: 1h) 
        ...
        """
        try:
            data = {}

            # Parse coin name and profit
            coin_match = re.search(r'⚠️\s*(\w+)\s*Профит за час:\s*([\d.]+)%', message_text)
            if coin_match:
                data['coin_name'] = coin_match.group(1).strip()
                data['hourly_profit'] = Decimal(coin_match.group(2))

            # Parse exchange rates
            exchanges = ['GATE', 'BINANCE', 'MEXC', 'OURBIT', 'BITGET', 'BYBIT']
            
            for exchange in exchanges:
                # Pattern for exchange rate
                pattern = rf'{exchange}\s*\(([^)]+)\):\s*([+-]?[\d.]+)%\s*\(интервал:\s*([^)]+)\)'
                match = re.search(pattern, message_text, re.IGNORECASE)
                
                if match:
                    url = match.group(1)
                    rate = Decimal(match.group(2))
                    interval = match.group(3).strip()

                    # Set exchange-specific fields
                    data[f'{exchange.lower()}_rate'] = rate
                    data[f'{exchange.lower()}_url'] = url
                    data[f'{exchange.lower()}_interval'] = interval

                    # Check for position (LONG/SHORT) - usually at the end
                    position_match = re.search(rf'{exchange}[^)]*\)[^)]*\((LONG|SHORT)\)', message_text, re.IGNORECASE)
                    if position_match:
                        data[f'{exchange.lower()}_position'] = position_match.group(1).upper()

            # Validate required fields
            if not data.get('coin_name'):
                return None

            return data

        except (ValueError, InvalidOperation, AttributeError) as e:
            logger.warning("Error parsing Funding Rate signal", error=str(e), message_preview=message_text[:100])
            return None
        except Exception as e:
            logger.error("Unexpected error parsing Funding Rate signal", error=str(e), exc_info=True)
            return None


class MEXCDEXParser(SignalParser):
    """Parser for MEXC & DEX Price Spread signals."""

    @staticmethod
    def parse(message_text: str) -> Optional[Dict[str, Any]]:
        """
        Parse MEXC & DEX signal from Telegram message.
        
        Format:
        🔴 YEE 13.9%

        Price Mxc (https://futures.mexc.com/exchange/YEE_USDT?inviteCode=1E5e4): 0.0221
        Price Dexscreener (https://dexscreener.com/ethereum/0x9Ac9468E7E3E1D194080827226B45d0B892C77Fd): 0.0190

        Max size | Deposit Withdrawal
         66$ | ✅ ✅

        Deposit (https://www.mexc.com/assets/deposit/YEE) | Withdrawal (https://www.mexc.com/assets/withdraw/YEE)
        ETH: 0x9Ac9468E7E3E1D194080827226B45d0B892C77Fd
        """
        try:
            data = {}

            # Parse coin name and spread (🔴 or 🟢 indicates direction)
            coin_match = re.search(r'[🔴🟢]\s*(\w+)\s*([\d.]+)%', message_text)
            if coin_match:
                data['coin_name'] = coin_match.group(1).strip()
                data['spread_percent'] = Decimal(coin_match.group(2))

            # Parse MEXC price
            mexc_match = re.search(r'Price Mxc[^:]*:\s*([\d.]+)', message_text, re.IGNORECASE)
            if mexc_match:
                data['mexc_price'] = Decimal(mexc_match.group(1))

            # Parse DEX price
            dex_match = re.search(r'Price Dexscreener[^:]*:\s*([\d.]+)', message_text, re.IGNORECASE)
            if dex_match:
                data['dex_price'] = Decimal(dex_match.group(1))

            # Extract URLs
            urls = SignalParser.extract_urls(message_text)
            for url in urls:
                if 'futures.mexc.com/exchange' in url:
                    data['mexc_url'] = url
                elif 'dexscreener.com' in url:
                    data['dexscreener_url'] = url
                elif 'mexc.com/assets/deposit' in url:
                    data['deposit_url'] = url
                elif 'mexc.com/assets/withdraw' in url:
                    data['withdrawal_url'] = url

            # Parse max size
            max_size_match = re.search(r'Max size[^$]*\$([\d.]+)', message_text, re.IGNORECASE)
            if max_size_match:
                data['max_size_usd'] = Decimal(max_size_match.group(1))

            # Parse deposit/withdrawal flags
            deposit_withdrawal_match = re.search(r'\$\s*\|\s*([✅❌])\s*([✅❌])', message_text)
            if deposit_withdrawal_match:
                data['deposit_enabled'] = deposit_withdrawal_match.group(1) == '✅'
                data['withdrawal_enabled'] = deposit_withdrawal_match.group(2) == '✅'

            # Parse token contract and chain
            chain_contract_match = re.search(r'(ETH|BSC|POLYGON|AVAX):\s*(0x[a-fA-F0-9]+)', message_text)
            if chain_contract_match:
                data['token_chain'] = chain_contract_match.group(1)
                data['token_contract'] = chain_contract_match.group(2)

            # Validate required fields
            if not data.get('coin_name'):
                logger.debug("MEXC & DEX signal missing coin_name")
                return None

            # Validate that we have price data
            if not data.get('mexc_price') or not data.get('dex_price'):
                logger.debug("MEXC & DEX signal missing price data")
                return None

            return data

        except (ValueError, InvalidOperation, AttributeError) as e:
            logger.warning("Error parsing MEXC & DEX signal", error=str(e), message_preview=message_text[:100])
            return None
        except Exception as e:
            logger.error("Unexpected error parsing MEXC & DEX signal", error=str(e), exc_info=True)
            return None


def detect_signal_type(message_text: str) -> Optional[str]:
    """Detect signal type from message text."""
    text_lower = message_text.lower()

    # MEXC Spot & Futures indicators
    if 'монета:' in text_lower and ('спред:' in text_lower or 'спот:' in text_lower):
        return 'mexc_spot_futures'

    # Funding Rate indicators
    if 'профит за час:' in text_lower or '⚠️' in message_text:
        return 'funding_rate'

    # MEXC & DEX indicators
    if ('🔴' in message_text or '🟢' in message_text) and 'price mxc' in text_lower:
        return 'mexc_dex'

    return None

