# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import pandas as pd
import json

from config import API_INTERVALS, BINANCE_FUTURES_API_URL, BINANCE_FUTURES_API_ENDPOINT
from utils.data_utils import convert_to_dict_financial_data


async def get_binance_futures_data(symbol, start_time, interval='1m', api_intervals=API_INTERVALS):
    """
    Асинхронная функция для получения данных фьючерсов с Binance Futures API.

    Arguments:
        symbol (str): Тикер для которого требуется получить данные.
        start_time (int): Время начала периода в миллисекундах для получения данных.
        interval (str, optional): Интервал времени для свечей. По умолчанию '1m'.
        api_intervals (dict, optional): Словарь, определяющий длительность интервалов в миллисекундах.

    Returns:
        dict: Словарь с данными, полученными от Binance Futures API.

    Usage Example:
        symbol = "BTCUSDT"
        start_time = 1609459200000  # Пример времени начала
        data = await get_binance_futures_data(symbol, start_time)

    Notes:
        Функция требует предварительного определения глобальных переменных
        `BINANCE_FUTURES_API_URL` и `BINANCE_FUTURES_API_ENDPOINT`, а также
        словаря `API_INTERVALS` с длительностями интервалов.
    """
    base_url = BINANCE_FUTURES_API_URL
    endpoint = BINANCE_FUTURES_API_ENDPOINT
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": start_time + api_intervals[interval]
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}{endpoint}", params=params) as response:
            data = await response.json()
            return data


async def get_signal_performance_data(symbol, alert_price, start_time, interval='1m', n_intervals=5,
                                      deviation_threshold=3, check_rise=True):
    """
    Асинхронная функция для анализа эффективности точки входа торгового сигнала на основе изменения цены относительно 'alert_price'.

    Arguments:
        symbol (str): Тикер для которого требуется получить данные.
        alert_price (float): Цена, на которой был сгенерирован сигнал.
        start_time (int): Время начала анализа в миллисекундах.
        interval (str, optional): Таймфрейм для данных. По умолчанию '1m'.
        n_intervals (int, optional): Количество интервалов для анализа. По умолчанию 5.
        deviation_threshold (float, optional): Порог отклонения цены в процентах для определения успешности сигнала.
                                               По умолчанию 3%.
        check_rise (bool, optional): Флаг для проверки роста цены (True) или ее падения (False). По умолчанию True.

    Returns:
        str: JSON строка, содержащая информацию о эффективности сигнала,
        включая изменение цены, статус и полученные данные.

    Usage Example:
        symbol = "BTCUSDT"
        alert_price = 120_000.0
        start_time = 1609459200000
        result = await get_signal_performance_data(symbol, alert_price, start_time, interval='1m', n_intervals=5, deviation_threshold=3, check_rise=True)

    Notes:
        - Функция использует 'get_binance_futures_data' для получения данных.
        - Статус 'Success' означает достижение ценой порога отклонения, 'Failure' - в противном случае.
    """

    price_change = None
    data = []
    # Запрашиваем данные для момента сигнала и для следующих интервалов
    for i in range(1, n_intervals+1):
        kline = i
        price_data = await get_binance_futures_data(symbol, start_time, interval)
        price_data = convert_to_dict_financial_data(price_data)
        data.append(price_data)
        if i == 1 and not (price_data['Low'] <= alert_price <= price_data['High']):
            status = f'alert_price not in low-high range'
            break

        # Выбор цены для проверки в зависимости от флага check_rise
        if check_rise:
            check_price = price_data['High']
        else:
            check_price = price_data['Low']

        # Сравнение open и close цен начинается со второго интервала
        if i > 1:
            if check_rise and price_data['Open'] >= price_data['Close']:
                status = "Failure"
                break
            elif not check_rise and price_data['Open'] <= price_data['Close']:
                status = "Failure"
                break

        price_change = (check_price - alert_price) / alert_price * 100  # Расчет процентного изменения

        # Проверка на достижение порога отклонения
        if abs(price_change) >= deviation_threshold:
            status = "Success"
            break

        # Обновляем время начала для следующего запроса
        start_time += API_INTERVALS[interval]

    return json.dumps({
        "kline": kline,
        "price_change": price_change,
        "status": status,
        "data": data
    }, indent=4)


async def get_previous_data(symbol, start_time, interval='1m', period=14, api_intervals=API_INTERVALS):
    """
    Асинхронно получает исторические данные о ценах для заданного символа с API Binance Futures.

    Arguments:
        symbol (str): Тикер для которого требуется получить данные.
        start_time (int): Время начала в миллисекундах, с которого начинается получение данных.
        interval (str, optional): Интервал времени для каждой точки данных. По умолчанию '1m'.
        period (int, optional): Количество интервалов для получения. По умолчанию 14.
        api_intervals (dict, optional): Словарь, определяющий длительность интервалов в миллисекундах.

    Returns:
        list: Список словарей с историческими данными о ценах за указанный период.

    Usage Example:
        symbol = "BTCUSDT"
        start_time = 1609459200000
        historical_data = await get_previous_data(symbol, start_time)

    Notes:
        - Функция использует 'get_binance_futures_data' для получения данных для каждого интервала.
        - Она итеративно вызывает API для сбора данных за указанное количество интервалов до предоставленного времени начала.
        - Полученные исторические данные используются для различных анализов, например, для расчета технических индикаторов, таких как RSI.
    """
    # Рассчитываем необходимое количество запросов для покрытия периода RSI
    historical_data = []
    for i in range(period+1):
        time = start_time - (period+1-i) * api_intervals[interval]
        price_data = await get_binance_futures_data(symbol, time, interval, api_intervals)
        price_data = convert_to_dict_financial_data(price_data)
        historical_data.append(price_data)

    return historical_data
