import requests
import json
from config import currency

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f'Введена неправильная или несуществующая валюта {quote}.')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(f'Введена неправильная или несуществующая валюта {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Число введено не корректно {amount}.')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/0e21bafe76ef27045298226f/pair/{quote_ticker}/{base_ticker}')
        total_base = json.loads(r.content)['conversion_rate']*amount

        return total_base
