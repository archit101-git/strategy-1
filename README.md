# Assets Traded

Cryptocurrencies: BTCUSD, ETHUSD
Stocks: AAPL, META, NVDA, TSM, INTU, BX, TSLA, PWR, NUE, ZM, NIO, BRKR, AXON, ODFL, PINS, EFX, BLDR, ENPH

# The following indicators are used for each active symbol:

Supertrend1: (Period: 10, Multiplier: 2.5, Moving Average: Wilders)
Supertrend2: (Period: 10, Multiplier: 3, Moving Average: Wilders)
RSI: (Period: 10, Moving Average: Wilders, Resolution: Daily)
EMA: (Period: 100, Resolution: Daily)
Weekly TWAP: (Period: 5 weeks, calculated using SMA)
Warm-Up Period
Warm-Up Period: 100 days
# Trading Logic

## Entry Conditions

A position is entered if the following conditions are met:

Current price is above both Supertrend1 and Supertrend2.
RSI is above 50.
Current price is above EMA100.
Current price is below a factor of the weekly TWAP (1.2 for cryptocurrencies and 1.04 for stocks).
## Exit Conditions

A position is exited if the current price falls below both Supertrend1 and Supertrend2.


