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

    text_in_patent = []

    results = driver.find_elements(By.CLASS_NAME, 'result.style-scope.search-result-item')

    for elements in results:
        elem = elements.find_element(By.XPATH, '//div[contains(@class, "search-result-item")]//raw-html[contains(@class, "search-result-item")]//span[contains(@class, "style-scope")]').text
        text_in_patent.append(elem)

    print(text_in_patent)


    for patent in results:
        title = patent.find_element(By.CSS_SELECTOR, '.style-scope.raw-html').text

        name = patent.find_element(By.CSS_SELECTOR, '.bullet-before.style-scope.search-result-item .style-scope.search-result-item .style-scope.raw-html').text

        date = patent.find_element(By.XPATH, '//h4[contains(@class, "dates")]').text

            # text_in_patent = patent.find_element(By.XPATH, '//div[contains(@class, "search-result-item")]//raw-html[contains(@class, "search-result-item")]//span[contains(@class, "style-scope")]').text



        # print(f'Title: {title},\nName autor patents: {name}\nDate: {date} \n\n')

finally:
    # Закрытие браузера
    driver.quit()

