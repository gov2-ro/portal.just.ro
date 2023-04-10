import time, sqlite3, csv, os, sys
from urllib.parse import urlparse, parse_qs
import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

""" 
for a list of instanțe,
loop days (excl weekends)
save nr sedinte to SQLite

TODO: save to sql more often, on each instanta? or.. make smaller batches?
TODO: make it resilient to errors!

TODO: how to stop when there's no sedinte? 
"Nu există nici o şedinţă." la câteva la rând?

 """

dbfile = '../data/just-scraping.db'
zitable = 'lista-sedinte'
# instante = [36,3,197]
instante = [197, 338, 3, 98]
instante = [197, 338]
 
start_date = '2022-3-01'
end_date = '2022-3-05'


def setup_method():
    driver = webdriver.Firefox()
    return driver

def teardown_method(driver):
    driver.quit()

def get_date(driver, url, date):
    zpath = "//div[@id='MSO_ContentTable']//div[@id='WebPartWPQ2']//table//td[contains(@class,'ms-dtinput')]//input[contains(@class,'ms-input')]"
    data = []
    next_page = 1 #read data table at least once.
    next_img_element = None
    
    # Wait for up to 10 seconds for the element to be present in the DOM
    wait = WebDriverWait(driver, 10)

    driver.get(url)
    input_field = driver.find_element(By.XPATH, zpath)
    input_field.clear()
    time.sleep(.3)
    input_field = driver.find_element(By.XPATH, zpath)
    input_field.send_keys(date)
    time.sleep(.3)
    input_field.send_keys(Keys.RETURN)
    
    
    # TODO: wait untill element arrives
 
    
    while next_page == 1:
         # TODO: wait untill element arrives
        time.sleep(.75)
        qdata_table = "//div[@id='WebPartWPQ3']//table[1]"
        qnext_table = "//div[@id='WebPartWPQ3']//table[2]"

         # check if ședințe, if not, skip.
        try:
           element = driver.find_element(By.XPATH, "//table[@class='s4-wpTopTable']//td[@class='ms-vb' and text()='Nu există nici o şedinţă.']")
           print('no sedinta for ' + date + url)
           return None
        except NoSuchElementException:
            pass

        # check if data table exists
        try:
            data_table = driver.find_element(By.XPATH, qdata_table)
        except NoSuchElementException:
            # stop the script TODO: log error
            print("Err: Element not found")
            return None

        # check if next element exists:
        # 1 - check if paging table exists 
        try:
            paging_table = driver.find_element(By.XPATH, qnext_table)
        except NoSuchElementException:
            # read data table only once.
            next_page = 0

        # 2 - check if link to next exists
        a_elements = paging_table.find_elements(By.TAG_NAME,"a") 
        if a_elements:
            last_a_element = a_elements[-1]
            next_img_element = last_a_element.find_elements(By.XPATH, ".//img[@src='/_layouts/images/next.gif'][@alt='Next']")
  
        else:
            print('stop next page')
            next_page = 0
        # Check if there are any 'a' elements and if the last one contains the specified image
        # if a_elements and a_elements[-1].find_element(By.XPATH, ".//img[@src='/_layouts/images/next.gif'][@alt='Next']"):
        #     # print("Last 'a' element contains the specified image.")
        #     next_page = 1
        # else:
        #     # print("No 'a' elements or last 'a' element does not contain the specified image.")
        #     next_page = 0

    
        # table_rows = driver.find_elements_by_xpath('//table/tbody/tr')
        table_rows = data_table.find_elements(By.TAG_NAME, "tr")

        # collect the data
        for row in table_rows:
            cols = row.find_elements(By.XPATH, './/td')
            if cols:
                row_data = {'departament': cols[0].text, 'complet': cols[1].text, 'ora': cols[2].text}
                # links = cols[0].find_elementss_by_xpath('.//a')
                links = cols[0].find_elements(By.XPATH, './/a')
                if links:
                    parsed_url = urlparse(links[0].get_attribute('href'))
                    query_params = parse_qs(parsed_url.query)
                    row_data['idx'] = query_params['id_sedinta'][0]
                # links = cols[1].find_elementss_by_xpath('.//a')
                # links = cols[1].find_elements(By.XPATH, './/a')
                # if links:
                #     row_data['complet_href'] = links[0].get_attribute('href')
                data.append(row_data)

        if next_img_element is not None and len(next_img_element):
    
            last_a_element.click()
            # print('clicked next')
            # TODO: wait untill element arrives
            time.sleep(1.1)
        else:
            next_page = 0  
    
    print('_____')
    return data


def generate_dates(start_date_str, end_date_str):
    # Convert the start and end date strings to date objects
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Define a function to check if a date is a weekend
    def is_weekend(date):
        return date.weekday() in [5, 6]  # 5 is Saturday and 6 is Sunday

    # Generate the list of dates, excluding weekends, and format them
    date_list = [
        (start_date + datetime.timedelta(days=x)).strftime('%d.%m.%Y')
        for x in range((end_date - start_date).days + 1)
        if not is_weekend(start_date + datetime.timedelta(days=x))
    ]

    return date_list

# def sedinte_instanta(id_instanta, zidate, driver):
#     driver = setup_method()
#     tdata = get_date(driver, "https://portal.just.ro/" + str(id_instanta) + "/SitePages/Lista_Sedinte.aspx?id_inst=179", zidate)
#     return tdata


if not os.access(dbfile, os.F_OK | os.W_OK):
    print("Database file does not exist or is not writable: " + dbfile)
    sys.exit(1) # Exit the script with error code 1

 
zirows = []
zidates = generate_dates(start_date, end_date)
driver = setup_method()


for id_instanta in instante:
    print('--instanta ' + str(id_instanta))
    for zidate in zidates:
        # breakpoint()
        print('---data: ' + str(zidate))
        newmeat = get_date(driver, "https://portal.just.ro/" + str(id_instanta) + "/SitePages/Lista_Sedinte.aspx?id_inst="  + str(id_instanta), zidate)
        if newmeat:
            zirows.extend(newmeat)


# tdata = get_date(driver, "https://portal.just.ro/3/SitePages/Lista_Sedinte.aspx?id_inst=3", "08.03.2023")

conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS "' + zitable + '" (institutie int, zi text, departament text, complet text, ora text, idx text)')

for row in zirows:
    date_obj = datetime.datetime.strptime(zidate, '%Y.%m.%d')
    c.execute("INSERT INTO \"" + zitable + "\" (departament, complet, ora, idx, institutie, zi) VALUES (:departament, :complet, :ora, :idx, :institutie, :zi)", {
        'departament': row['departament'],
        'complet': row['complet'],
        'ora': row['ora'],
        'idx': row['idx'],
        'institutie': id_instanta,  
        'zi': date_obj.date().isoformat()  
    })


conn.commit()
conn.close()

print('saved to db')
teardown_method(driver)


 
