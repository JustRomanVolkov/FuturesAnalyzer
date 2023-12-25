# -*- coding: utf-8 -*-
import asyncio
import json

from api.binance_api import get_signal_performance_data, get_previous_data, API_INTERVALS

from utils.data_utils import extract_price, convert_to_dict_financial_data, get_previous_close_price_for_rsi
from utils.finance_utils import calculate_rsi
from utils.time_utils import convert_time_to_utc_millis

from visualization.plot_utils import visualize_entry_point


if __name__ == "__main__":
    """Исходные данные"""
    symbol = 'ARUSDT'  # Тикер
    alert_price = 'alert price: 8.006'  # Цена сигнала
    start_time = '2023-11-09 18:23:54.181000'  # Стартовое время сигнала

    """Подготовка исходных данных"""
    # Извлечение числового значения цены из строки
    clear_price = extract_price(alert_price)
    # Конвертация локального времени в миллисекунды UTC
    clear_time = convert_time_to_utc_millis(start_time)

    """Расчет RSI"""
    # Получение исторических данных для расчета RSI
    historical_data = asyncio.run(get_previous_data(symbol, clear_time, interval='1m', period=14))

    # Извлечение списка цен закрытия для расчета RSI
    close_prices_list = get_previous_close_price_for_rsi(historical_data)

    # Расчет RSI и вывод его значений
    rsi = calculate_rsi(close_prices_list, period=14)
    print(json.loads(rsi))

    """ Получение данных об эффективности сигнала """
    result = asyncio.run(get_signal_performance_data(
        symbol, clear_price, clear_time, interval='1m', n_intervals=7,
        deviation_threshold=4, check_rise=False
    ))
    # Десериализация строки JSON в словарь для дальнейшего анализа
    result_dict = json.loads(result)
    print(result_dict)

    """визуализация данных - свечной график с указанием цены сигнала"""
    price_data = result_dict["data"]
    # Визуализация точки входа на основе полученных данных
    visualize_entry_point(symbol, price_data, clear_price)
