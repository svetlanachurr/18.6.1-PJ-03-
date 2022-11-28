import requests


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(_from: str, to: str, amount: int):
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={_from}&tsyms={to}')
        result_json = r.json()
        result = result_json[to]

        return result * amount
