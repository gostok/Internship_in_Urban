import pandas as pd
import os

def export_data_to_csv(data, filename):
    """
    Сохраняет загруженные данные об акциях в CSV файл.

    :param data: DataFrame с данными об акциях.
    :param filename: Имя файла, в который будут сохранены данные.
    """
    os.makedirs('stock_files/csv_files', exist_ok=True)
    filepath = os.path.join('stock_files/csv_files', filename)
    data.to_csv(filepath, index=True, encoding='utf-8')

    print(f"График сохранен в {filepath}")