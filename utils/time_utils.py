# -*- coding: utf-8 -*-
import pytz
from dateutil import parser


def convert_time_to_utc_millis(time_str, timezone='Europe/Moscow'):
    """
    Преобразует строку с датой и временем в количество миллисекунд с начала эпохи UTC.

    Аргументы:
        time_str (str): Строка с датой и временем для преобразования.
        timezone (str, optional): Часовой пояс, в котором находится время. По умолчанию 'Europe/Moscow'.

    Возвращает:
        int: Количество миллисекунд с начала эпохи UTC.

    Пример использования:
        time_str = "2023-11-09 20:13:00.304000"
        millis = convert_time_to_utc_millis(time_str)
        millis == 1699549980304 # соответствующее количество миллисекунд

    Примечания:
        - Функция использует библиотеки 'dateutil' и 'pytz' для разбора строки и работы с временными зонами.
        - Время сначала локализуется в заданной временной зоне, затем преобразуется в UTC.
        - Подходит для использования в случаях, когда необходимо преобразовать локальное время в универсальное
        координированное время (UTC) и получить его представление в миллисекундах.
    """
    # Разбор строки даты и времени
    local_time = parser.parse(time_str)

    # Получение объектов временных зон
    local_tz = pytz.timezone(timezone)
    utc_tz = pytz.utc

    # Локализация времени в заданной временной зоне
    local_time = local_tz.localize(local_time)

    # Конвертация времени в UTC
    utc_time = local_time.astimezone(utc_tz)

    # Конвертация времени в миллисекунды
    utc_time_millis = int(utc_time.timestamp() * 1000)
    return utc_time_millis
