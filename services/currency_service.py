import config

class CurrencyService:
    def __init__(self):
        self.rates = {
            'USD': 1.0,
            'EUR': 0.95,
            'MAD': 10.0
        }
        self.symbols = {
            'USD': '$',
            'EUR': '€',
            'MAD': 'DH'
        }
        self.current_currency = config.DEFAULT_CURRENCY

    def set_currency(self, currency_code):
        if currency_code in self.rates and currency_code in config.SUPPORTED_CURRENCIES:
            self.current_currency = currency_code

    def convert(self, amount_usd):
        rate = self.rates.get(self.current_currency, 1.0)
        return amount_usd * rate

    def format(self, amount_usd):
        converted = self.convert(amount_usd)
        symbol = self.symbols.get(self.current_currency, '$')
        
        if self.current_currency == 'MAD':
            return f"{converted:.2f} {symbol}"
        elif self.current_currency == 'EUR':
            return f"{symbol}{converted:.2f}"
        else:
            return f"{symbol}{converted:.2f}"
