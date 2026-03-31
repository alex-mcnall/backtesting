import datetime, numpy

import pytest, yfinance

from currency_converter.yfinance import YahooFinanceConverter

def test_symbol_lookup_gbpusd():
    '''Test the symbol lookup for GBP to USD works'''
    converter = YahooFinanceConverter()
    symbol = converter._identify_ticker("GBP", "USD")
    assert symbol == "GBPUSD=X"

def test_symbol_lookup_usdgbp():
    '''Test the symbol lookup for USD to GBP works'''
    converter = YahooFinanceConverter()
    symbol = converter._identify_ticker("USD", "GBP")
    assert symbol == "GBP=X"

def test_symbol_lookup_usdusd():
    '''Test for an error when trying to convert to the original currency'''
    converter = YahooFinanceConverter()
    with pytest.raises(ValueError):
        symbol = converter._identify_ticker("USD", "USD")

def test_exchange_rate_usdgbp():
    '''Check that the USD/GBP exchange gives the correct value'''
    converter = YahooFinanceConverter()
    ticker = yfinance.Ticker("GBP=X")

    # Set a date where the market is open (to avoid an empty dataframe)
    date = datetime.datetime(2025, 3, 21)
    
    # Get the most recent close price
    price = ticker.history(start=date, period="1d")["Close"].iloc[-1]

    # Check the converter gives the close price for the date given
    assert converter.get_exchange_rate("USD", "GBP", date) == price


def test_exchange_rate_gbpusd():
    '''Check that the GBP/USD exchange gives the correct value'''
    converter = YahooFinanceConverter()
    ticker = yfinance.Ticker("GBPUSD=X")

    # Set a date where the market is open (to avoid an empty dataframe)
    date = datetime.datetime(2025, 3, 21)
    
    # Get the most recent close price
    price = ticker.history(start=date, period="1d")["Close"].iloc[-1]

    # Check the converter gives the close price for the date given
    assert converter.get_exchange_rate("GBP", "USD", date) == price

def test_exchange_rate_date_datetime():
    '''Check that the GBP/USD exchange gives the correct value'''
    converter = YahooFinanceConverter()
    ticker = yfinance.Ticker("GBPUSD=X")

    # Create datetime and date objects
    date = datetime.datetime(2025, 3, 21, 15, 24, 31, 12)
    date2 = datetime.date(2025, 3, 21)

    # Check they give the same result
    assert converter.get_exchange_rate("GBP", "USD", date) == converter.get_exchange_rate("GBP", "USD", date2)

def test_exchange_rate_return_type():
    '''Check that the returned exchange rate is a numpy float'''
    converter = YahooFinanceConverter()
    assert isinstance(converter.get_exchange_rate("GBP", "RUB"), numpy.floating)

def test_date_weekend_gives_week_close():
    '''
    Check that the rates on a Saturday is the Friday close price.

    The Sunday close price would not be the same because the market reopens at
    17:00 UTC.
    '''
    converter = YahooFinanceConverter()

    # Create datetime and date objects
    date = datetime.date(2026, 3, 20) # Friday
    date2 = datetime.date(2026, 3, 21) # Saturday

    # Check they give the same result
    assert converter.get_exchange_rate("GBP", "USD", date) == converter.get_exchange_rate("GBP", "USD", date2)

def test_error_unknown_currency():
    '''Test an exception is thrown for a nonexistant currency'''
    converter = YahooFinanceConverter()
    with pytest.raises(Exception):
        symbol = converter._identify_ticker("GBP", "Nonexistant Currency")
