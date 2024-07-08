from AlgorithmImports import *

class TopCryptoStrategy(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2024, 3, 1)  # Set Start Date
        self.SetEndDate(2024, 6, 1)
        self.SetCash(100000)  # Set Strategy Cash

        # Define the symbols
        self.crypto_symbols = ["BTCUSD", "ETHUSD"]
        self.stock_symbols = ["AAPL","META", "NVDA","TSM","INTU","BX" "TSLA", "PWR", "NUE","ZM", "NIO", "BRKR", "AXON", "ODFL", "PINS", "EFX","BLDR","ENPH"]
        self.SetBenchmark("SPY")

        # Attempt to add each cryptocurrency and stock
        self.active_symbols = []
        for symbol in self.crypto_symbols:
            try:
                self.AddCrypto(symbol, Resolution.Daily)
                self.active_symbols.append(symbol)
            except Exception as e:
                self.Debug(f"Unable to add symbol: {symbol}. Exception: {e}")

        for symbol in self.stock_symbols:
            try:
                self.AddEquity(symbol, Resolution.Daily)
                self.active_symbols.append(symbol)
            except Exception as e:
                self.Debug(f"Unable to add symbol: {symbol}. Exception: {e}")

        # Define the technical indicators
        self.supertrend1 = {}
        self.supertrend2 = {}
        self.rsi = {}
        self.ema100 = {}
        self.weekly_twap = {}
        self.entry_prices = {}

        for symbol in self.active_symbols:
            self.supertrend1[symbol] = self.STR(symbol, 10, 2.5, MovingAverageType.Wilders)
            self.supertrend2[symbol] = self.STR(symbol, 10, 3, MovingAverageType.Wilders)
            self.rsi[symbol] = self.RSI(symbol, 10, MovingAverageType.Wilders, Resolution.Daily)
            self.ema100[symbol] = self.EMA(symbol, 100, Resolution.Daily)
            self.weekly_twap[symbol] = self.WeeklyTwap(symbol, 5)
            self.entry_prices[symbol] = None

        self.SetWarmUp(100, Resolution.Daily)  # Warm up period for 100 days

    def WeeklyTwap(self, symbol, num_weeks):
        twap = self.SMA(symbol, num_weeks * 5, Resolution.Daily)  # Assuming 5 trading days per week
        return twap

    def OnData(self, data):
        if self.IsWarmingUp:
            return

        for symbol in self.active_symbols:
            if not data.Bars.ContainsKey(symbol):
                continue

            bar = data.Bars[symbol]

            # Get current values
            current_price = bar.Close
            supertrend1 = self.supertrend1[symbol].Current.Value
            supertrend2 = self.supertrend2[symbol].Current.Value
            rsi = self.rsi[symbol].Current.Value
            ema100 = self.ema100[symbol].Current.Value
            weekly_twap = self.weekly_twap[symbol].Current.Value

            # Define factor based on asset type
            factor = 1.2 if symbol in self.crypto_symbols else 1.04

            # Entry condition
            if self.entry_prices[symbol] is None:
                if (current_price > supertrend1 and 
                    current_price > supertrend2 and 
                    rsi > 50 and 
                    current_price > ema100 and 
                    current_price < factor * weekly_twap):  # Use appropriate factor
                    self.Debug(f"{symbol}: Supertrend1={supertrend1}, Supertrend2={supertrend2}, RSI={rsi}, EMA100={ema100}, Weekly TWAP={weekly_twap}")
                    self.SetHoldings(symbol, 0.2)
                    self.entry_prices[symbol] = current_price

            # Exit condition
            elif current_price < supertrend1 and current_price < supertrend2:
                self.Liquidate(symbol)
                self.entry_prices[symbol] = None