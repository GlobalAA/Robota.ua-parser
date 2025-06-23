import time
from typing import Dict, List, Set, Tuple

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_last_page(driver: WebDriver) -> Tuple[int, Dict[str, int]]:
	try:
		last_page: WebElement = WebDriverWait(driver, 4).until(
			EC.presence_of_element_located(
				(By.XPATH, '//div[contains(@class, "paginator")]//a[normalize-space(text())][last()]')
			)
		)
		return int(last_page.text), last_page.location

	except (TimeoutException, NoSuchElementException):
		return 0, {"x": 0, "y": 0}
	
def parsing(driver: WebDriver, data: List[dict[str, str]], current_height: int, max_height: int):
	parsed_links: Set[str] = set() 

	while current_height <= max_height:
		vacancy_blocks = driver.find_elements(By.CSS_SELECTOR, "alliance-vacancy-card-desktop")

		for block in vacancy_blocks:
			try:
				link: str | None = block.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
				if link in parsed_links:
					continue
				if link is None:
					continue

				parsed_links.add(link)

				title = block.find_element(By.CSS_SELECTOR, "h2").text.strip()
				company = block.find_element(By.CSS_SELECTOR, "span.santa-mr-20").text.strip()

				data.append({
					"Заголовок": title,
					"Компанія": company,
					"Посилання": link
				})
			except Exception as e:
				pass 

		if (current_height and max_height) == 0:
			break

		driver.execute_script("window.scrollBy(0, window.innerHeight);")
		current_height = driver.execute_script("return window.pageYOffset + window.innerHeight")
		time.sleep(1.5)

	return data