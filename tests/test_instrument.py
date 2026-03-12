import pytest

from instrument import Instrument

def test_instrument_name(sample_instrument):
    name = "Advanced Micro Devices"
    assert sample_instrument.name == name


def test_instrument_symbol(sample_instrument):
    ticker = "AMD"
    assert sample_instrument.ticker == ticker
