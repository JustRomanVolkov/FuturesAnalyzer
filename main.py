# -*- coding: utf-8 -*-
import asyncio
import json

from api.binance_api import get_signal_performance_data, get_previous_data, API_INTERVALS

from utils.data_utils import extract_price, convert_to_dict_financial_data, get_previous_close_price_for_rsi
from utils.finance_utils import calculate_rsi
from utils.time_utils import convert_time_to_utc_millis

from visualization.plot_utils import visualize_entry_point


if __name__ == "__main__":

    # 12,ARUSDT,💥💥💥,1 kline,alert price: 8.006,2023-11-09 18:23:54.181000
    # 75,CELRUSDT,🌊🌊🌊,2 kline,alert price: 0.01566,2023-11-09 20:13:00.304000

    symbol = 'CELRUSDT'
    alert_price = 'alert price: 0.01455'
    start_time = '2023-11-09 20:13:00.304000'

    clear_price = extract_price(alert_price)
    clear_time = convert_time_to_utc_millis(start_time)

    print(f"{symbol} {clear_price}: {clear_time}")

    historical_data = asyncio.run(get_previous_data(symbol, clear_time, interval='1m', period=14, api_intervals=API_INTERVALS))
    print(historical_data)

    close_prices_list = get_previous_close_price_for_rsi(historical_data)
    print(close_prices_list)
    rsi = calculate_rsi(close_prices_list, period=14)
    print(json.loads(rsi))


    result = asyncio.run(get_signal_performance_data(symbol, clear_price, clear_time, interval='3m', n_intervals=7,
                                          deviation_threshold=4, check_rise=False))
    # Десериализация строки JSON обратно в словарь
    result_dict = json.loads(result)
    print(result_dict)

    price_data = result_dict["data"]
    visualize_entry_point(symbol, price_data, clear_price)









