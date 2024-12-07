def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия акций за заданный период.

    :param data: DataFrame с историческими данными об акциях.
    """
    average_price = data['Close'].mean()
    print(f"Средняя цена закрытия акций за заданный период: {average_price:.2f}")
