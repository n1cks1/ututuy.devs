
import requests
from bs4 import BeautifulSoup
import time
import json

count = 0 #считаю кол-во цитат, просто проверка
quotesList = []  #сюда сохраняю все цитаты

for i in range(1, 11): #на сайте всего 10 страниц, поэтому такой цикл
    url = f"https://quotes.toscrape.com/page/{i}" #пагинация
    response = requests.get(url) #дефолтный запрос
    time.sleep(2)  #задержка чтобы не забанило

    if response.status_code == 200: #здесь проверка на правильную отдачу запроса
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.findAll('div', class_='quote')

        for quote in quotes:
            data = {
                "text": quote.find('span', class_='text').text,
                "author": quote.find("small", class_="author").text
            }
            quotesList.append(data)  # Добавляю цитату в список

            count += 1            
    else:
        print(f"Ошибка при получении страницы {url}")
    
print(f"Всего собрано цитат: {count}")


with open('quotes.json', 'w' , encoding='utf-8') as f: #сораняю в (quotes.json, тип "запись", кодировка)
    json.dump(quotesList, f, ensure_ascii=False, indent=4) #сохраняю цитаты в (список цитат, файл, чтобы принимало кириллицу, табуляция)
        
print("Цитаты сохранены в файл quotes.json")


