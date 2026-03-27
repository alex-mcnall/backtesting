import datetime
from abc import ABC, abstractmethod

class CurrencyConverterService(ABC):
    '''
    Abstract class to enforce a common interface that each currency converter
    service class must adhere to.
    '''
    @abstractmethod
    def get_exchange_rate(self, base: str, quote: str, date: datetime.datetime | datetime.date | None):
        raise NotImplementedError
