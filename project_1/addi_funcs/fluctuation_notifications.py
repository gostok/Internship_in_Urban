
def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет о значительных колебаниях цен акций.

    Функция анализирует данные о ценах закрытия акций и проверяет,
    превышает ли процентное изменение между максимальной и минимальной
    ценами заданный порог. Выводит уведомление с информацией о ценах
    и процентном изменении.

    Параметры:
    ----------
    data : pandas.DataFrame
        DataFrame с данными о ценах акций, включая колонку 'Close'.

    threshold : float
        Пороговое значение в процентах для уведомления о колебаниях.
    """
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    price_change_percentage = ((max_price - min_price) / min_price) * 100

    if price_change_percentage > threshold:
        print(f"Уведомление: Цена акций колебалась более чем на {threshold}% за период. "
              f"Максимальная цена: {max_price:.2f}, Минимальная цена: {min_price:.2f}, "
              f"Изменение: {price_change_percentage:.2f}%")
    else:
        print(f"Цена акций не колебалась более чем на {threshold}%.")
