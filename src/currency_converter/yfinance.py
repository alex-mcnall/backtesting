import datetime

import yfinance

from .currency_converter import CurrencyConverter

class YahooFinanceConverter(CurrencyConverter):
    '''
    Use the yfinance module to get currency conversion rates using Yahoo Finance's forex data.
    '''
    # Allow users to refer to this converter as "yfinance"
    _service_key = "yfinance"

    @staticmethod
    def _identify_ticker(base: str, quote: str) -> str:
        '''
        Attempt to identify the Yahoo Finance forex symbol for the given
        currencies.

        Parameters
        ----------
        base : str
            The currency that the value is being converted from.
        quote: str
            The currency that the value is being converted to.

        Returns
        -------
        str
            The ticker for the identified forex pair.
        '''
        MAX_COUNT = 50

        # Check that the symbols are not the exact same
        if base == quote:
            raise ValueError(f"Base and quote currencies are identical: {base}")

        # Make a guess for the currency pair name (e.g GBP/USD)
        guess = base + "/" + quote
        
        # Perform lookup for currency pair
        search = yfinance.Lookup(guess).get_currency(count=MAX_COUNT)

        # Check if search not empty
        if not search.empty:
            # If an exact match is found, return its symbol
            if search["shortName"].iloc[0] == guess:
                return search["shortName"].index[0]

        # If it isn't found, give up and throw an exception
        raise Exception(f"Yahoo Finance could not find a currency pair for the base and quote currencies {base} and {quote} respectively")
    
    def get_exchange_rate(
        self,
        base,
        quote,
        date: datetime.datetime | datetime.date | None = None,
    ) -> float:
        '''
        Get the exchange rate between the base and quote currencies

        Recover exchange rates from Yahoo Finance forex tickers. This method
        calls another method to find the correct ticker before getting the
        forex price history. A simple check to see if recent price information
        exists is performed. If no recent price information can be found, an
        exception is thrown.

        Parameters
        ----------
        base : str
            The currency that the value is being converted from.
        quote: str
            The currency that the value is being converted to.
        date: {date, datetime, None}, optional
            The time to use for the exchange rate. If None, then default to
            the most recent exchange rate.

        Returns
        -------
        float
            Forex rate at the close of the price interval (minute, day, etc.)
        '''

        # Recover the correct forex pair
        ticker = YahooFinanceConverter._identify_ticker(base, quote)

        # Truncate datetime to day (yfinance only provides daily values)
        if isinstance(date, datetime.datetime):
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Create ticker object
        yf_ticker = yfinance.Ticker(ticker)

        # Attempt to recover price
        price_data = yf_ticker.history(start=date, period="1d")
        
        # Check if a value was returned
        if price_data.empty:
            # Check for prices for the previous two weeks
            price_data = yf_ticker.history(end=date, period="14d")

            if price_data.empty:
                raise Exception(f"No price information is available for the last two weeks for {ticker}.")

        return price_data['Close'].iloc[-1]

