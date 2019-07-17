from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
driver = webdriver.Chrome()
driver.get("https://www.amazon.com/Acroprint-01-0182-000-ES700-Electronic-Accommodates/dp/B000GR9STG/ref=sr_1_1_sspa?keywords=Electronics%2C+Computers+%26+Office&qid=1562994039&s=gateway&sr=8-1-spons&psc=1")
description = driver.find_element_by_xpath("//*[@id='feature-bullets']/ul")
items = description.find_elements_by_tag_name('li')
for i in items:
    print(i.text)