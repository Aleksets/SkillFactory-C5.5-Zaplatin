import json
import requests
from config import keys


# класс пользовательских исключений
class APIException(Exception):
    pass


# класс преобразования валюты (с отслеживанием исключений)
class GetPrice:
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException("Необходимо вводить разные валюты!")
        if base not in keys.keys():
            raise APIException(f"Валюта {base} отсутствует в базе!")
        if quote not in keys.keys():
            raise APIException(f"Валюта {quote} отсутствует в базе!")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"{amount} не является числом")
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={keys[base]}&tsyms={keys[quote]}")
        total_base = json.loads(r.content)[keys[quote]] * amount
        return total_base


# класс корректировки вывода названий валют для облегчения чтения
class Out:
    @staticmethod
    def correct(argument):
        if argument == "евро":
            return argument
        elif argument == "доллар":
            return "доллар(а/ов)"
        elif argument == "рубль":
            return "рубль(я/ей)"
