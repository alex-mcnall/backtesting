import datetime

from .yahoo_finance_converter import YahooFinanceConverter


class CurrencyConverter():
    '''
    Currency converter which can use multiple services to retrieve data.

    Description to be written.

    Parameters
    ----------
    service : string, optional
        String which is used to identify which currency converter to use.
        Defaults to the service given by _default_service.

    Attributes
    ----------
    service : string
        The string identifier for the currency converter service. The getter
        method returns the string. The setter method updates the string and
        retrieves the class which implements the service, so new converter
        objects will use the new class. This does not create an object, so
        each method which uses the routine is responsible for creating a
        temporary object.

    Methods
    ----------
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
    np.float64(124.63078498840332)
    '''
    _services = {
            "yfinance": YahooFinanceConverter
            }
    _default_service = "yfinance"

    def __init__(self, service: str = _default_service):
        # Set the service
        self.service = service

    @property
    def service(self):
        '''Get the name of the service in use'''
        return self._service_name
    
    @service.setter
    def service(self, service: str = _default_service):
        '''Recovers the service class and sets the name'''
        # Check if the service is a valid one
        if service in self._services:
            # Recover the service class
            self._service = self._services.get(service)

            # Set the service name string
            self._service_name = service
        else:
            raise ValueError(f"Unknown currency converter service: {service}")

    def convert(
        self,
        value: float,
        base: str,
        quote: str,
        date: datetime.datetime | datetime.date | None = None,
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
        rate = self._service().get_exchange_rate(base, quote, date)
        return value*rate
