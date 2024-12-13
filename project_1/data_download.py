import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period='1mo', start_date=None, end_date=None):
    """
    Получает исторические данные акций для указанного тикера.

    :param
    - ticker (str): Тикер акции, для которой необходимо получить данные.
    - period (str, optional): Период для получения данных (по умолчанию '1mo').
    - start_date (str, optional): Дата начала в формате 'YYYY-MM-DD' (по умолчанию None).
    - end_date (str, optional): Дата окончания в формате 'YYYY-MM-DD' (по умолчанию None).

    :return
    - pandas.DataFrame: Исторические данные акций в виде DataFrame, содержащий информацию о ценах (открытие, закрытие, максимумы, минимумы и объем) за указанный период или за указанные даты.

    Исключения:
    - ValueError: Если указаны некорректные даты или тикер.
    """
    stock = yf.Ticker(ticker)

    if start_date and end_date:
        data = stock.history(start=start_date, end=end_date)
    else:
        data = stock.history(period=period)

    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def add_rsi(data, window=5):
    """
    Добавляет индекс относительной силы (RSI) к данным акций.

    :param data: DataFrame с данными акций.
    :param window: Период для расчета RSI.
    :return: DataFrame с добавленным столбцом 'RSI'.
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data


def add_macd(data):
    """
    Добавляет индикатор MACD и сигнальную линию к данным акций.

    :param data: DataFrame с данными акций.
    :return: DataFrame с добавленными столбцами 'MACD' и 'Signal_Line'.
    """
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    return data
