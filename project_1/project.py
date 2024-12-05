import os
import json


class PriceMachine():
    
    def __init__(self):
        self.data = []
        self.result = ''
        self.name_length = 0
    
    def load_prices(self, file_path=''):
        '''
            Сканирует указанный каталог. Ищет файлы со словом price в названии.
            В файле ищет столбцы с названием товара, ценой и весом.
            Допустимые названия для столбца с товаром:
                товар
                название
                наименование
                продукт
                
            Допустимые названия для столбца с ценой:
                розница
                цена
                
            Допустимые названия для столбца с весом (в кг.)
                вес
                масса
                фасовка
        '''
        count_files = 0
        count_lines = 0
        self.data = []
        current_path = os.path.dirname(os.path.realpath(__file__))
        if not file_path:
            file_path = current_path
        for file_name in os.listdir(file_path):
            if 'price' in file_name :
                count_files += 1
                print('read',file_name)
                with open(os.path.join(file_path, file_name), 'r') as f:
                    headers = f.readline()
                    product_name_number, price_number, weight_number = self._search_product_price_weight(headers)
                    file_data = f.readlines()
                    for line in file_data:
                        count_lines += 1
                        line_data = line.split(',')
                        product_name = line_data[product_name_number].strip().lower()
                        if len(product_name) > self.name_length:
                            self.name_length = len(product_name)
                        price = int(line_data[price_number].strip())
                        weight = int(line_data[weight_number].strip())
                        value = round(price / weight,2)
                        self.data.append((value, product_name, price, weight, file_name))
        self.data.sort()
        return count_files, count_lines
        
    def _search_product_price_weight(self, headers):
        '''
            Возвращает номера столбцов
        '''
        data = headers.lower().strip().split(',')
        product_name_number = '!'
        for index in range(len(data)):
            if data[index] in ('товар','название','продукт','наименование'):
                product_name_number = index
            if data[index] in ('розница','цена'):
                price_number = index
            if data[index] in ('вес','масса','фасовка'):
                weight_number = index
        return product_name_number, price_number, weight_number

    def export_to_html(self, fname='output.html'):
        result = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        '''
        for number, item in enumerate(self.data):
            value, product_name, price, weight, file_name = item
            result += '<tr>' 
            result += f'<td>{number + 1}</td>' 
            result += f'<td>{product_name}</td>' 
            result += f'<td>{price}</td>' 
            result += f'<td>{weight}</td>' 
            result += f'<td>{file_name}</td>' 
            result += f'<td>{value}</td>' 
            result += '</tr>\n' 
        result += '</tbody>'
        result += '</table>'
        print(fname)
        with open(fname, 'w') as f:
            f.write(result)
        return 'ok'
    
    def find_text(self, text):
        text = text.lower()
        data = [item for item in self.data if text in item[1]]
        data.sort()
        return data

    
pm = PriceMachine()
print(pm.load_prices())
while 1:
    command = input('Введите exit для выхода или часть названия для поиска: \n')
    if command == 'exit':
        break
    else:
        name = command
        res = pm.find_text(name)
        print(f'{"№": <4}  {"Наименование": <{pm.name_length}} {"цена":^5} {"вес":^3} {"файл":^12} {"цена за кг."}')
        for number, item in enumerate(res):
            print(f'{number + 1: <4}  {item[1]: <{pm.name_length}} {item[2]:^5}  {item[3]:^3} {item[4]:^12} {item[0]}')
print('the end')
print(pm.export_to_html())


'''
добавить в условие "цена за кг и сортировка"
развитие задания: 
'''
