import numpy
from unittest import mock

import pytest

from currency_converter import CurrencyConverter


@mock.patch("currency_converter.yfinance.YahooFinanceConverter.get_exchange_rate")
def test_convert(mock_get_exchange_rate):
    '''
    Test that the returned value uses the exchange rate given by a stub
    converter object.
    '''
    mock_get_exchange_rate.return_value = numpy.float64(1.244)
    
    converter = CurrencyConverter()
    assert converter.convert(100.0, "GBP", "USD") == numpy.float64(124.4)

def test_service():
    '''
    Test that the service is assigned correctly and returns the string that
    identifies it (rather than the class itself).
    '''
    converter = CurrencyConverter("yfinance")
    assert converter.service == "yfinance"

def test_unknown_service():
    '''Check that unknown services give a ValueError.'''
    converter = CurrencyConverter()
    with pytest.raises(ValueError):
        CurrencyConverter("random")
    with pytest.raises(ValueError):
        CurrencyConverter("Does not exist")
    with pytest.raises(ValueError):
        CurrencyConverter("Y.finance")
    with pytest.raises(ValueError):
        CurrencyConverter("y-finance")
