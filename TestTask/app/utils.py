# Конвертор валют. Принимает код двух валют и количество обмениваемой валюты
from typing import Optional

import requests
from bs4 import BeautifulSoup


class Converter:
    url = "https://www.banki.ru/products/currency/cb/"  # ссылка для парсинга

    def __init__(self, from_exchange: str, to_exchange: str, value: Optional[int | float]):
        self.from_exchange = from_exchange
        self.to_exchange = to_exchange
        self.value = value

    @staticmethod
    def __parse(url) -> BeautifulSoup:
        """Парсинг с сайта"""
        req = requests.get(url)
        src: str = req.text
        return BeautifulSoup(src, "lxml")

    def __parse_filter(self, country_code) -> list[int | str]:
        """Фильтрация валюты по ее коду, возвращает курс в рублях"""
        if country_code.upper() == "RUB":
            result = [1, "RUB"]
        else:
            soup = self.__parse(self.url)
            countries = soup.find('tr', {"data-currency-code": country_code.upper()})
            result = countries.text.split()
        return result

    def calculation(self) -> float:
        """Калькулятор валюты"""
        from_cash: list[int | str] = self.__parse_filter(self.from_exchange)
        to_cash: list[int | str] = self.__parse_filter(self.to_exchange)
        result: float = round(float(from_cash[-2]) * float(self.value) / float(to_cash[-2]), 2)
        return result
