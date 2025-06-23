import logging
import os
from typing import List

import pandas as pd
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from utils import get_last_page, parsing

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
load_dotenv()

VACANCY: str = os.getenv("VACANCY", "Python")
COUNTRY: str = os.getenv("COUNTRY", "Ukraine")
SUFFIX_FILE: str = os.getenv("SUFFIX_FILE", "_request")

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

driver = webdriver.Firefox(options=options)
driver.delete_all_cookies()
driver.maximize_window()

def main():
	try:
		logging.info("Парсинг розпочато!")
		driver.get(f'https://robota.ua/zapros/{VACANCY}/{COUNTRY.lower()}/params;page=1') 
		
		index, location = get_last_page(driver)

		page_list: List[int] = [i+1 for i in range(1, index)]
		current_height = 0
		max_height = location['y'] + 1500 if location["y"] > 0 else location["y"]


		data = []

		parsing(driver, data, current_height, max_height)

		if page_list:
			for i in page_list:
				driver.get(f'https://robota.ua/zapros/{VACANCY}/{COUNTRY.lower()}/params;page={i}') 

				parsing(driver, data, current_height, max_height)

		df = pd.DataFrame(data)
		filename = f"{VACANCY}_{COUNTRY.capitalize()}{SUFFIX_FILE}.csv"
		df.to_csv(filename, index=False)

		logging.info("Парсинг завершено")
		logging.info(f"Усього вакансій: {len(data)}")
		logging.info(f"Дані збережено у файл: {filename}")


	except TimeoutException:
		logging.error("Timed out waiting for page to load")
	finally:
		driver.quit()

if __name__ == "__main__":
	main()