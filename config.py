# -*- coding: utf-8 -*-

BINANCE_FUTURES_API_URL = "https://fapi.binance.com"
BINANCE_FUTURES_API_ENDPOINT = "/fapi/v1/klines"


API_INTERVALS = {
    "1m": 60_000,  # 1 минута
    "3m": 180_000,  # 3 минуты
    "5m": 300_000,  # 5 минут
    "15m": 900_000,  # 15 минут
    "30m": 1_800_000,  # 30 минут
    "1h": 3_600_000,  # 1 час
    "2h": 7_200_000,  # 2 часа
    "4h": 14_400_000,  # 4 часа
    "6h": 21_600_000,  # 6 часов
    "8h": 28_800_000,  # 8 часов
    "12h": 43_200_000,  # 12 часов
    "1d": 86_400_000,  # 1 день
    "3d": 259_200_000,  # 3 дня
    "1w": 604_800_000,  # 1 неделя
}

KLINE_DATA_KEYS = (
    "Open_time",
    "Open",
    "High",
    "Low",
    "Close",
    "Volume",
    "Close_time",
    "Quote_asset_volume",
    "Number_of_trades",
    "Taker_buy_base_asset_volume",
    "Taker_buy_quote_asset_volume",
    "Ignore"
)
