import pytest
from services.currency_service import CurrencyService
import config

def test_currency_conversion():
    service = CurrencyService()
    service.set_currency("MAD")
    # 10.0 is the rate for MAD in the service
    assert service.convert(10) == 100.0

def test_currency_formatting():
    service = CurrencyService()
    
    service.set_currency("USD")
    assert service.format(10) == "$10.00"
    
    service.set_currency("MAD")
    assert service.format(10) == "100.00 DH"

def test_unsupported_currency():
    service = CurrencyService()
    original_currency = service.current_currency
    service.set_currency("JPY") # Not in config.SUPPORTED_CURRENCIES or rates
    assert service.current_currency == original_currency
