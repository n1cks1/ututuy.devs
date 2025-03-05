from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox()

driver.get('https://patents.google.com/?q=te+OR+(invention)&language=SPANISH')

try:

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'result.style-scope.search-result-item'))
    )

    results = driver.find_elements(By.CLASS_NAME, 'result.style-scope.search-result-item')

    for patent in results:
        title = patent.find_element(By.CSS_SELECTOR, '.style-scope.raw-html').text

        name = patent.find_element(By.CSS_SELECTOR, '.bullet-before.style-scope.search-result-item .style-scope.search-result-item .style-scope.raw-html').text

        print(f'Название патента: {title},\n name autor patents: {name}\n\n')

finally:
    # Закрытие браузера
    driver.quit()

