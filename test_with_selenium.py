from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json

# Инициализация драйвера
firefox_dev_path = r'C:\Program Files\Firefox Developer Edition\firefox.exe'

options = webdriver.FirefoxOptions()
options.binary_location = firefox_dev_path


driver = webdriver.Firefox(options=options)

# Открываем страницу
# driver.get('https://patents.google.com/?q=te+OR+(invention)&language=SPANISH&num=50')

urls = [
    'https://patents.google.com/?q=("energía+renovable"+OR+"energía+solar"+OR+"energía+eólica")&language=SPANISH&num=50&oq="energía+renovable"+OR+"energía+solar"+OR+"energía+eólica"+language:SPANISH&page=',
    'https://patents.google.com/?q=(%22tratamiento+m%C3%A9dico%22+OR+%22dispositivo+m%C3%A9dico%22+OR+%22f%C3%A1rmaco%22)&language=SPANISH&num=50&oq=%22tratamiento+m%C3%A9dico%22+OR+%22dispositivo+m%C3%A9dico%22+OR+%22f%C3%A1rmaco%22+language:SPANISH&page=',
    'https://patents.google.com/?q=(%22inteligencia+artificial%22+OR+%22aprendizaje+autom%C3%A1tico%22+OR+%22red+neuronal%22)&language=SPANISH&num=50&oq=%22inteligencia+artificial%22+OR+%22aprendizaje+autom%C3%A1tico%22+OR+%22red+neuronal%22+language:SPANISH&page=',
    'https://patents.google.com/?q=(%22modelo+de+utilidad%22+OR+%22utilidad+pr%C3%A1ctica%22)&language=SPANISH&num=50&page=',
    'https://patents.google.com/?q=(%22veh%C3%ADculo+el%C3%A9ctrico%22+OR+%22transporte+aut%C3%B3nomo%22+OR+%22sistema+de+navegaci%C3%B3n%22)&language=SPANISH&num=50&oq=%22veh%C3%ADculo+el%C3%A9ctrico%22+OR+%22transporte+aut%C3%B3nomo%22+OR+%22sistema+de+navegaci%C3%B3n%22+language:SPANISH&page=',
    'https://patents.google.com/?q=(%22dise%C3%B1o+industrial%22+OR+%22modelo+de+utilidad%22+OR+%22patente+de+dise%C3%B1o%22)&language=SPANISH&num=50&page='
]

patents_data = []
countPage = 0
count = 0
try:
    for url in urls:
        try:
            for num in range(20):
                link_for_pars = url + str(num)
                countPage += 1
                print(link_for_pars)
                print(countPage)

                driver.get(link_for_pars)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'result.style-scope.search-result-item'))
                )

                results = driver.find_elements(By.CLASS_NAME, 'result.style-scope.search-result-item')

                for patent in results:
                    title = patent.find_element(By.CSS_SELECTOR, '.style-scope.raw-html').text
                    full_date = patent.find_element(By.XPATH, './/h4[contains(@class, "dates")]').text 
                    for part in full_date.split("•"):
                        if "Published" in part:
                            date = part.replace("Published", "").strip() #strip() убирает пробелы, без него будут пробелы в начале даты
                            break

                    spans = patent.find_elements(By.ID, 'htmlContent')
                    text_patent = spans[-1].text

                    count+=1

                    patents_data.append({
                        "title": title,
                        "date": date,
                        "text_patent": text_patent,
                    })

                    # print(f'Title: {title},\nDate: {date},\nText patent: {text_patent}\n\n')
                print(count)

        except TimeoutException:
            print(f"Ошибка: TimeoutException при обработке ссылки {link_for_pars}. Переход к следующей ссылке.")
            continue
        except Exception as e:
            print(f"Ошибка при обработке ссылки {link_for_pars}: {e}. Переход к следующей ссылке.")
            continue

finally:
    driver.quit()

with open('patents.json', 'w', encoding='utf-8') as f:
    json.dump(patents_data, f, ensure_ascii=False, indent=4)

print("Данные патентов сохранены в файл patents.json")
print(f'Количество записей = {count}')
