import time
from urllib.parse import urljoin

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

BASE = "https://alarabi.nccal.gov.kw"
URL = "https://alarabi.nccal.gov.kw/Home/SectionDetails/69?page={}"

# driver = uc.Chrome(headless=True)
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(version_main=140, options=options, headless=True)

all_links = set()

for page in range(1, 6):
    driver.get(URL.format(page))
    time.sleep(3)  # allow Cloudflare / JS to finish

    elements = driver.find_elements(By.CSS_SELECTOR, 'a[href^="/Home/Article"]')
    print(elements)
    for e in elements:
        href = e.get_attribute("href")
        if href:
            all_links.add(urljoin(BASE, href))

driver.quit()

for link in sorted(all_links):
    print(link)
