from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Инициализация драйвера
driver = webdriver.Firefox()

# Открываем страницу
driver.get('https://patents.google.com/?q=te+OR+(invention)&language=SPANISH&num=50')

patents_data = [] 

try:
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


        # Добавляем данные в список
        patents_data.append({
            "title": title,
            "date": date,
            "text_patent": text_patent,
        })

        print(f'Title: {title},\nDate: {date},\nText patent: {text_patent}\n\n')

finally:
    # Закрытие браузера
    driver.quit()

# Сохраняем данные в JSON файл
with open('patents.json', 'w', encoding='utf-8') as f:
    json.dump(patents_data, f, ensure_ascii=False, indent=4)

print("Данные патентов сохранены в файл patents.json")
