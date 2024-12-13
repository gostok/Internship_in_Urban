import data_download as dd
import data_plotting as dplt
from addi_funcs.calculate_price import calculate_and_display_average_price
from addi_funcs.fluctuation_notifications import notify_if_strong_fluctuations
from addi_funcs.data_to_csv import export_data_to_csv

def main():
    """
    Основная функция для запуска приложения по получению и анализу данных акций.

    Эта функция:
    - Приветствует пользователя и предоставляет информацию о доступных тикерах и периодах.
    - Запрашивает у пользователя тикер акции и (опционально) даты начала и окончания для анализа.
    - Получает данные акций с использованием функции `fetch_stock_data`.
    - Добавляет вычисления, такие как скользящее среднее, RSI и MACD, к данным.
    - Строит график на основе полученных данных.
    - Вычисляет и отображает среднюю цену закрытия акций.
    - Экспортирует данные акций в CSV файл.
    - Уведомляет пользователя о сильных колебаниях цен акций, если они превышают заданный порог.

    Входные данные:
    - Пользователь вводит тикер акции, даты начала и окончания (или выбирает период).

    Примечания:
    - Если даты не указаны, пользователь может ввести период для получения данных.
    - В случае некорректного ввода данных, функция может уведомить пользователя о проблемах.
    """
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")

    # Запрос на ввод дат
    start_date = input("Введите дату начала в формате YYYY-MM-DD (или оставьте пустым для предустановленного периода): ")
    end_date = input("Введите дату окончания в формате YYYY-MM-DD (или оставьте пустым для предустановленного периода): ")

    # Проверка на пустые значения
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None

    print(start_date, end_date, sep="\n")

    # Если даты не указаны, запрашиваем период
    if not start_date and not end_date:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        stock_data = dd.fetch_stock_data(ticker, period=period)
    else:
        stock_data = dd.fetch_stock_data(ticker, start_date=start_date, end_date=end_date)

    # Добавляем скользящее среднее к данным
    stock_data = dd.add_moving_average(stock_data)
    stock_data = dd.add_rsi(stock_data)
    stock_data = dd.add_macd(stock_data)

    # Строим график
    dplt.create_and_save_plot(stock_data, ticker, start_date, end_date)

    # Выводим среднюю цену закрытия
    calculate_and_display_average_price(stock_data)

    # Загружаем данные об акциях в CSV файл.
    export_data_to_csv(stock_data, f'{ticker}_{start_date}_{end_date}')

    notify_if_strong_fluctuations(stock_data, threshold=5)  # Уведомление при колебаниях более 5%



if __name__ == "__main__":
    main()
