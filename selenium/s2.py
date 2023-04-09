from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def setup_method():
    driver = webdriver.Firefox()
    return driver

def teardown_method(driver):
    driver.quit()

def test_pj3(driver, url, date):
    zpath = "//div[@id='MSO_ContentTable']//div[@id='WebPartWPQ2']//table//td[contains(@class,'ms-dtinput')]//input[contains(@class,'ms-input')]"
    driver.get(url)
    input_field = driver.find_element(By.XPATH, zpath)
    input_field.clear()
    time.sleep(.2)
    input_field = driver.find_element(By.XPATH, zpath)
    input_field.send_keys(date)
    time.sleep(.2)
    input_field.send_keys(Keys.RETURN)


driver = setup_method()
test_pj3(driver, "https://portal.just.ro/57/SitePages/Lista_Sedinte.aspx?id_inst=57", "04.04.2023")

breakpoint()
teardown_method(driver)
