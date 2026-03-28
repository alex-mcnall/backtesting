import datetime
from abc import ABC, abstractmethod

class CurrencyConverterService(ABC):
    '''
    Abstract class to provide a consistent interface for the CurrencyConverter
    class to interact with currency converter services.
    '''
    @abstractmethod
    def get_exchange_rate(
        self,
        base: str,
        quote: str,
        date: datetime.datetime | datetime.date | None = None,
    ) -> float:
        '''
        Get the exchange rate between the base and quote currencies

        Uses the selected backend to get the exchange rate between the base
        and quote currencies. A date or datetime object can optionally be
        supplied to use a historical exchange rate. By default, if no date is
        supplied, the most recent close value is used. For historical data,
        the close value on or before the supplied date is used. An exception
        should be thrown if no exchange rate is found.

        Parameters
        ----------
        base : str
            The currency that the value is being converted from.
        quote : str
            The currency that the value is being converted to.
        date : {date, datetime, None}, optional
            The time to use for the exchange rate. If None, then default to
            the most recent exchange rate.

        Returns
        -------
        float
            Forex rate at the close of the price interval (minute, day, etc.)
        '''
        raise NotImplementedError
