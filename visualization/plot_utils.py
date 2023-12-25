# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import mplfinance as mpf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker


def visualize_entry_point(symbol, price_data, alert_price):
    """
    Визуализирует точку входа на графике цен для заданного торгового символа.

    Arguments:
        symbol (str): Торговый символ, который будет отображаться на графике.
        price_data (list of dict): Список словарей с данными о ценах.
        alert_price (float): Цена, которая будет выделена на графике.

    Usage Example:
        symbol = "BTCUSDT"
        price_data = [{'Open_time': 1609459200000, 'Open': 1, 'High': 2, 'Low': 0.5, 'Close': 1.5, 'Volume': 100}, ...]
        alert_price = 1.5
        visualize_entry_point(symbol, price_data, alert_price)

    Notes:
        - Функция использует библиотеку mplfinance для создания свечного графика.
        - Данные преобразуются в DataFrame и адаптируются для соответствия формату, требуемому mplfinance.
        - Линия alert_price добавляется на график для визуального выделения заданной цены.
        - Функция предназначена для визуального анализа ценовых данных и может быть использована для технического анализа на финансовых рынках.
    """
    # Конвертация данных в DataFrame
    df = pd.DataFrame(price_data)
    df['Open_time'] = pd.to_datetime(df['Open_time'], unit='ms')
    df.set_index('Open_time', inplace=True)

    # Создание графика с данными свечей и объемом
    fig, axlist = mpf.plot(df, type='candle', volume=True, style='charles', returnfig=True, figscale=1.0, title=f"{symbol} Price Chart")

    # Настройка точности оси y
    axlist[0].yaxis.set_major_formatter(mticker.FormatStrFormatter('%.5f'))

    # Добавление линии alert_price
    axlist[0].axhline(alert_price, color='red', linestyle='--')

    # Аннотация для линии alert_price
    axlist[0].annotate(f'Alert Price: {alert_price}', xy=(0.5, 0.9), xycoords='axes fraction', fontsize=12, color='red', ha='center')

    # Показ графика
    mpf.show()
