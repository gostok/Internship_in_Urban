import data_download as dd
import data_plotting as dplt
from addi_funcs.calculate_price import calculate_and_display_average_price
from addi_funcs.fluctuation_notifications import notify_if_strong_fluctuations
from addi_funcs.data_to_csv import export_data_to_csv

def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)

    # Выводим среднюю цену закрытия
    calculate_and_display_average_price(stock_data)

    # Загружаем данные об акциях в CSV файл.
    export_data_to_csv(stock_data, f'{ticker}_{period}')

    notify_if_strong_fluctuations(stock_data, threshold=5)  # Уведомление при колебаниях более 5%


if __name__ == "__main__":
    main()
