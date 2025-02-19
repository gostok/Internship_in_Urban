import os
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

def create_and_save_plot(data, ticker, period, filename=None, style='seaborn'):
    """
    Создает и сохраняет график цен акций с техническими индикаторами.

    :param data: DataFrame с данными акций и индикаторами.
    :param ticker: Тикер акции для заголовка графика.
    :param period: Период, за который загружаются данные.
    :param filename: Имя файла для сохранения графика (по умолчанию генерируется автоматически).
    :param style: Стиль оформления графика (по умолчанию 'seaborn').
    """
    os.makedirs('stock_files', exist_ok=True)

    # Применяем выбранный стиль
    plt.style.use(style)

    # Создаем фигуру с тремя подграфиками
    fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

    # График цен акций и скользящей средней
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            axs[0].plot(dates, data['Close'].values, label='Close Price')
            axs[0].plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        axs[0].plot(data['Date'], data['Close'], label='Close Price')
        axs[0].plot(data['Date'], data['Moving_Average'], label='Moving Average')

    axs[0].set_title(f"{ticker} Цена акций с течением времени")
    axs[0].set_ylabel("Цена")
    axs[0].legend()

    # График RSI
    if 'RSI' in data:
        axs[1].plot(data.index, data['RSI'], label='RSI', color='orange')
        axs[1].axhline(70, linestyle='--', alpha=0.5, color='red', label='Overbought (70)')
        axs[1].axhline(30, linestyle='--', alpha=0.5, color='green', label='Oversold (30)')
        axs[1].set_title('Индекс относительной силы (RSI)')
        axs[1].set_ylabel("RSI")
        axs[1].legend()

    # График MACD
    if 'MACD' in data:
        axs[2].plot(data.index, data['MACD'], label='MACD', color='green')
        axs[2].plot(data.index, data['Signal_Line'], label='Signal Line', color='red')
        axs[2].set_title('MACD')
        axs[2].set_ylabel("MACD")
        axs[2].legend()

    # График стандартного отклонения
    if 'Standard Deviation' in data:
        std_dev = data['Standard Deviation'].iloc[0]  # Получаем стандартное отклонение
        axs[0].axhline(y=std_dev, color='red', linestyle='--', label='Стандартное отклонение')
        axs[0].legend()

    plt.xlabel("Дата")

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    filepath = os.path.join('stock_files', filename)
    plt.tight_layout()
    plt.savefig(filepath)
    print(f"График сохранен как {filename}")


def create_interactive_plot(data, ticker):
    """
    Создает интерактивный график с использованием Plotly.

    :param data: DataFrame с данными акций.
    """

    # Вычисляем среднее значение колонки 'Close'
    average_close = data['Close'].mean()
    print(f'Среднее значение цены закрытия для '
          f'{data.index[-1].date()}: {average_close:.2f}')

    # Создаем интерактивный график
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'],
                             mode='lines', name='Цена закрытия'))

    # Добавляем линию для скользящего среднего, если оно существует
    if 'Moving_Average' in data:
        fig.add_trace(go.Scatter(x=data.index, y=data['Moving_Average'],
                                 mode='lines', name='Скользящее среднее'))

    fig.update_layout(title=f'График акций {ticker}',
                      xaxis_title='Дата',
                      yaxis_title='Цена',
                      legend_title='Легенда')

    fig.show()