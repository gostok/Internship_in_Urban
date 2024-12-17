

def calculate_standard_deviation(data):
    """
    Рассчитывает стандартное отклонение цены закрытия.

    Параметры:
    data (DataFrame): DataFrame с историческими данными акций.

    Возвращает:
    float: Стандартное отклонение цены закрытия.
    """
    return data['Close'].std()

def add_standard_deviation(data):
    """
    Добавляет стандартное отклонение цены закрытия в DataFrame.

    Параметры:
    data (DataFrame): DataFrame с историческими данными акций.

    Возвращает:
    DataFrame: Обновленный DataFrame с добавленным стандартным отклонением.
    """
    std_dev = calculate_standard_deviation(data)
    data['Standard Deviation'] = std_dev
    return data
