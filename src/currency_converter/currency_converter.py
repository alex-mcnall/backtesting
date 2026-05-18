import datetime, numpy
from abc import ABC, abstractmethod

class CurrencyConverter(ABC):
    '''
    Currency converter which can use multiple services to retrieve data.

    Parameters
    ----------
    service : string, optional
        String which is used to identify which currency converter to use.
        Defaults to the service given by _default_service.

    Attributes
    ----------
    service : string
        The string identifier for the currency converter service. The getter
        method returns the string. The service cannot be updated. A new
        instance of the class should be created

    Methods
    ----------
    get_exchange_rate(base, quote, date=None)
        Get the exchange rate from the ``base`` currency to the ``quote``
        currency a specified ``date``, or current rate if no date is provided.
    converter(value, base, quote, date=None)
        Convert ``value`` from the ``base`` currency to the ``quote` currency
        and return this value.

    Raises
    ----------
    ValueError
        If an unknown currency converter ``service`` name is supplied.

    Examples
    ----------
    >>> c = CurrencyConverter("yfinance")
    >>> c.convert(100.0, "GBP", "USD", datetime.date(2023, 4, 7))
    >>> c
    np.float64(124.39001798629761)
    '''
    _services = {}

    def __init_subclass__(cls, **kwargs):
       '''Called when any subclass is created.'''
       # Identify the key stored in the subclass
       key = getattr(cls, '_service_key', cls.__name__)

       # Retrieve the subclass
       CurrencyConverter._services[key] = cls

    def __new__(cls, service = "yfinance"):
        # Allow invoking the converter service directly instead of via this class.
        if cls is not CurrencyConverter:
            return super().__new__(cls)

        # Get the service name
        service_class = CurrencyConverter._services.get(service)
        if service_class is None:
            raise ValueError(f"Unknown currency converter service: {service}")

        return super().__new__(service_class)

    @property
    def service(self):
        '''Return the string that identifies the converter service in use'''
        return self.__class__._service_key

    @abstractmethod
    def get_exchange_rate(
        self,
        base: str,
        quote: str,
        date: Optional[Union[datetime.datetime, datetime.date]],
    ) -> numpy.floating:
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

    def convert(
        self,
        value: float,
        base: str,
        quote: str,
        date: Optional[Union[datetime.datetime, datetime.date]] = None,
    ) -> float:
        """
        Convert a value from the base currency to the quote currency.

        Convert a value from the base currency to the quote currency using the
        selected service. A date or datetime object can optionally be supplied
        to use a historical exchange rate.

        Parameters
        ----------
        value : float
            The amount of units of the the base currency.
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
            The given value converted from the base currency to the quote currency
        """
        # Create converter service object and get exchange rate
        rate = self.get_exchange_rate(base, quote, date)
        return value*rate
