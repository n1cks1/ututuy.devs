from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Firefox()

driver.get('https://patents.google.com/?q=te+OR+(invention)&language=SPANISH')

patents_data = []  # Список для хранения данных о патентах

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'result.style-scope.search-result-item'))
    )

    results = driver.find_elements(By.CLASS_NAME, 'result.style-scope.search-result-item')

    for patent in results:
        title = patent.find_element(By.CSS_SELECTOR, '.style-scope.raw-html').text
        name = patent.find_element(By.CSS_SELECTOR, '.bullet-before.style-scope.search-result-item .style-scope.search-result-item .style-scope.raw-html').text
        date = patent.find_element(By.XPATH, '//h4[contains(@class, "dates")]').text
        

        # Добавляем данные в список
        patents_data.append({
            "title": title,
            "name": name,
            "date": date
        })

        print(f'Title: {title},\nName autor patents: {name}\nDate: {date} \n\n')

finally:
    # Закрытие браузера
    driver.quit()

# Сохраняем данные в JSON файл
with open('patents.json', 'w', encoding='utf-8') as f:
    json.dump(patents_data, f, ensure_ascii=False, indent=4)

print("Данные патентов сохранены в файл patents.json")

