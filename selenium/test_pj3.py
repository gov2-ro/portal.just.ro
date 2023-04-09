# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

 
def setup_method(self):
  self.driver = webdriver.Firefox()
  self.vars = {}
  
def teardown_method(self):
  self.driver.quit()

def test_pj3(self, url, date):
  self.driver.get(url)
  zpath = "//div[@id='MSO_ContentTable']//div[@id='WebPartWPQ2']//table//td[contains(@class,'ms-dtinput')]//input[contains(@class,'ms-input')]"
  input_field = self.driver.find_element(By.XPATH, zpath)
  input_field.clear()
  time.sleep(.2)
  input_field = self.driver.find_element(By.XPATH, zpath)
  input_field.send_keys(date)
  time.sleep(.2)
  input_field.send_keys(Keys.RETURN)
    
setup_method(None)
test_pj3('https://portal.just.ro/57/SitePages/Lista_Sedinte.aspx?id_inst=57', '05.04.2023')

breakpoint()
teardown_method(None)

# if __name__ == '__main__':
#     test = TestPj3()
#     test.setup_method(None)
#     test.test_pj3('https://portal.just.ro/57/SitePages/Lista_Sedinte.aspx?id_inst=57', '05.04.2023')
#     breakpoint()
#     test.teardown_method(None)
