# -*- coding: utf-8 -*-
import re

import pandas as pd

from config import KLINE_DATA_KEYS


def extract_price(price):
    """
    Извлекает числовое значение цены из строки.

    Arguments:
        price (str): Строка, содержащая числовое значение цены, возможно, смешанное с другими символами.

    Returns:
        float: Числовое значение цены, извлеченное из строки.

    Usage Example:
        price_str = "alert price: 5.201."
        price = extract_price(price_str)
        # price == 5.201

    Notes:
        - Функция использует регулярные выражения для поиска первого вхождения числового значения в строке.
        - Поддерживает извлечение как целых чисел, так и чисел с плавающей точкой.
        - Если в строке нет числовых значений, функция может вызвать исключение.
    """
    price = float(re.search(r"\d+(\.\d+)?", price).group(0))
    return price


def convert_to_dict_financial_data(data, keys=KLINE_DATA_KEYS):
    """
    Преобразует список финансовых данных в словарь с ключами, соответствующими определенным меткам.

    Arguments:
        data (list): Список, содержащий финансовые данные (обычно извлекается из API).
        keys (tuple, optional): Кортеж строк, представляющих ключи для словаря. По умолчанию KLINE_DATA_KEYS.

    Returns:
        dict: Словарь с финансовыми данными, где ключи соответствуют заданным меткам.

    Usage Example:
        data = [['1609459200000', '1', '2', '0.5', '1.5', '100', ...], ...]
        financial_dict = convert_to_dict_financial_data(data)

    Notes:
        - Функция предполагает, что 'data' - это список списков, где каждый внутренний список содержит данные одной свечи.
        - Каждый элемент данных преобразуется в float, если содержит десятичную точку, иначе в int.
        - Функция полезна для стандартизации и упрощения обработки финансовых данных, получаемых из API.
    """
    formatted_item = map(lambda x: float(x) if '.' in str(x) else int(x), data[0])
    result = dict(zip(keys, formatted_item))
    return result


def get_previous_close_price_for_rsi(historical_data):
    """
    Извлекает список закрытия цен из исторических данных для расчета индекса относительной силы (RSI).

    Arguments:
        historical_data (list of dict): Список словарей, содержащих исторические данные о ценах.

    Returns:
        list: Список цен закрытия из исторических данных.

    Usage Example:
        historical_data = [{'Open_time': 1609459200000, 'Open': 1, 'High': 2, 'Low': 0.5, 'Close': 1.5, 'Volume': 100}, ...]
        close_prices = get_previous_close_price_for_rsi(historical_data)

    Notes:
        - Функция предполагает, что каждый элемент списка 'historical_data' содержит ключ 'close'.
        - Полученный список цен закрытия используется для дальнейших расчетов, например, для вычисления RSI.
    """
    df = pd.DataFrame(historical_data)
    close_prices_list = df['Close'].tolist()
    return close_prices_list
