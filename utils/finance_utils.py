# -*- coding: utf-8 -*-
import json
import pandas as pd


def calculate_rsi(prices, period=14):
    """
    Вычисляет индекс относительной силы (RSI) для списка цен.

    Arguments:
        prices (list of float): Список цен для расчета RSI.
        period (int, optional): Период, на основе которого рассчитывается RSI. По умолчанию равен 14.

    Returns:
        str: JSON строка, содержащая список значений RSI.

    Usage Example:
        prices = [45.34, 46.09, 45.91, 46.23, 45.78, 46.03, 45.61, 46.28, 46.28, 46.00, 45.66, 46.33, 46.29, 46.15]
        rsi_json = calculate_rsi(prices)
        # rsi_json == JSON строка со списком RSI

    Notes:
        - RSI рассчитывается путем сравнения средних значений прироста и потерь цен за определенный период.
    """
    # Преобразование списка цен в DataFrame
    df = pd.DataFrame(prices, columns=['price'])

    # Вычисление изменений цен
    delta = df['price'].diff()

    # Разделение на положительные и отрицательные изменения
    gain = (delta.clip(lower=0)).fillna(0)
    loss = (-delta.clip(upper=0)).fillna(0)

    # Вычисление среднего значения прибылей и убытков
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    # Расчет RS и RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Заполнение начальных значений RSI как None, так как они не определены
    rsi[:period] = None

    # Возвращение RSI в формате JSON
    return json.dumps({"rsi_list": rsi.tolist()}, indent=4)
