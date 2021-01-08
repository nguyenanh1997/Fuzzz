from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS()
driver.get("http://testphp.vulnweb.com/search.php?test=")
if "mysql" in driver.page_source:

    print(driver.page_source)
else:
    print("khong co loi")