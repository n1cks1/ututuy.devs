import json
from datetime import datetime


completed_file = 'patents.json'


with open(completed_file, 'r', encoding='utf-8') as f: # здесь из нового только буква r - означает чтение файла
    data_set = json.load(f)


def date_range():
    min_date = None # тут обязательно None, просто 0 не работает, тк это объект
    max_date = None

    for date in data_set:
        # strptime первым аргументом берет дату из файла и делает из него объект datetime, 
        # вторым аргументом берет формат даты из файла, нужно указать самим
        current_date = datetime.strptime(date['date'], '%Y-%m-%d')
            
        if(min_date == None) or (current_date < min_date):
            min_date = current_date

        # Обновляем максимальную дату
        if(max_date == None) or (current_date > max_date): 
            max_date = current_date

    # Преобразуем даты обратно в строки
    start_date = min_date.strftime('%Y-%m-%d') # strftime - делает из объекта datetime строку в нашем же формате даты
    end_date = max_date.strftime('%Y-%m-%d')
        
    print(f"Диапазон дат: с {start_date} по {end_date}")

date_range()