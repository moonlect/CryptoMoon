from app.services.telegram.parsers import FundingRateParser

sample = '''Parser (название еще не придумали) [CheapMirror], [16.12.2025 10:03]
⚠️ RAVE Профит за час: 0.4576%
GATE (https://www.gate.com/uk/futures/USDT/RAVE_USDT): -0.4563% (интервал: 1.0h) (LONG)
BINANCE (https://www.binance.com/en/futures/RAVEUSDT): 0.005% (интервал: 4h) (SHORT)
MEXC (https://futures.mexc.com/exchange/RAVE_USDT): 0.005% (интервал: 4h) 
OURBIT (https://futures.ourbit.com/exchange/RAVE_USDT): 0.005% (интервал: 4h) 
BITGET (https://www.bitget.com/ru/futures/usdt/RAVEUSDT): -0.0076% (интервал: 4h) 
BYBIT (https://www.bybit.com/trade/usdt/RAVEUSDT): 0.005% (интервал: 4h)
'''

res = FundingRateParser.parse(sample)
print(res)
