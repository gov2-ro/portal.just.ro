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

TODO: catch <span class="ms-error">Trebuie introdusă o valoare pentru acest filtru.</span>

 """

dbfile = '../data/just-scraping.db'
zitable = 'lista-sedinte'
# instante = [36,3,197]
# instante = [197, 338, 3, 98]
instante = [57,107,175,176,191,203,298,97,195,221,240,243,272,278,85,174,257,294,306,787,32,110,180,199,260,270,829,103,188,279,291,321,64,62,1372,197,226,293,338,119,248,305,322,2,81,3,753,92,299,300,301,4,302,303,116,202,249,269,98,229,312,330,122,192,236,93,94,1748,87,292,329,335,339,740,33,112,186,190,265,117,752,1285,211,219,235,242,328,100,182,224,307,319,336,84,309,337,1752,36,118,212,254,256,842,88,179,253,327,54,63,183,201,215,230,304,95,263,267,317,318,101,181,225,274,313,332,104,184,207,213,311,44,113,196,228,247,121,233,316,324,838,91,173,231,275,45,99,739,866,239,245,286,89,189,244,333,35,111,177,187,255,271,833,83,218,266,46,109,1259,205,214,216,280,828,90,185,198,223,241,42,114,200,277,282,287,105,204,259,281,310,331,120,232,262,283,284,315,39,40,193,217,222,297,86,206,227,237,285,314,334,43,96,234,258,268,326,102,1371,251,289,308,320,323,59,108,210,238,246,250,55,115,208,261,273,290,751,30,832,220,252,295,325]
 
start_date = '2023-3-01'
end_date = '2023-3-31'

def setup_method():
    driver = webdriver.Firefox()
    return driver

def teardown_method(driver):
    driver.quit()

def get_date(driver, id_instanta, date, conn, zitable):
    zpath = "//div[@id='MSO_ContentTable']//div[@id='WebPartWPQ2']//table//td[contains(@class,'ms-dtinput')]//input[contains(@class,'ms-input')]"
    data = []
    next_page = 1 #read data table at least once.
    next_img_element = None
    
    # Wait for up to 10 seconds for the element to be present in the DOM
    wait = WebDriverWait(driver, 10)
    url = "https://portal.just.ro/" + str(id_instanta) + "/SitePages/Lista_Sedinte.aspx?id_inst="  + str(id_instanta)
    driver.get(url) #TODO: what to do on 404?
    input_field = driver.find_element(By.XPATH, zpath)
    input_field.clear()
    time.sleep(.3)
    input_field = driver.find_element(By.XPATH, zpath)
    input_field.send_keys(date)
    time.sleep(.3)
    input_field.send_keys(Keys.RETURN)
    
    c = conn.cursor()
    
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

        table_rows = data_table.find_elements(By.TAG_NAME, "tr")

        # collect the data
        for row in table_rows:
            cols = row.find_elements(By.XPATH, './/td')
            if cols:
                row_data = {'departament': cols[0].text, 'complet': cols[1].text, 'ora': cols[2].text}
                links = cols[0].find_elements(By.XPATH, './/a')
                if links:
                    parsed_url = urlparse(links[0].get_attribute('href'))
                    query_params = parse_qs(parsed_url.query)
                    row_data['idx'] = query_params['id_sedinta'][0]

                row_data['zi'] = date
                row_data['institutie'] = id_instanta
                data.append(row_data)

        if next_img_element is not None and len(next_img_element):    
            last_a_element.click()
            # TODO: wait untill element arrives
            time.sleep(1.1)
        else:
            next_page = 0  
    
    for row in data:
        date_obj = datetime.datetime.strptime(zidate, '%d.%m.%Y') 
        c.execute("INSERT INTO \"" + zitable + "\" (departament, complet, ora, sedinta, institutie, zi) VALUES (:departament, :complet, :ora, :sedinta, :institutie, :zi)", {
            'departament': row['departament'],
            'complet': row['complet'],
            'ora': row['ora'],
            'sedinta': row['idx'],
            'institutie': id_instanta,  
                'zi': date_obj.date().isoformat()  
            })   

    conn.commit()
    print('\_/\_/')

    return None


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

if not os.access(dbfile, os.F_OK | os.W_OK):
    print("Database file does not exist or is not writable: " + dbfile)
    sys.exit(1) # Exit the script with error code 1
 
zirows = []
zidates = generate_dates(start_date, end_date)
driver = setup_method()
conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS "' + zitable + '" (institutie int, zi text, departament text, complet text, ora text, sedinta int)')

for id_instanta in instante:
    print('--instanta ' + str(id_instanta))
    for zidate in zidates:
        # breakpoint()
        print('---data: ' + str(zidate))
        get_date(driver, id_instanta, zidate, conn, zitable)
    
conn.close()
# tdata = get_date(driver, "https://portal.just.ro/3/SitePages/Lista_Sedinte.aspx?id_inst=3", "08.03.2023")

os.system('say "all Done"')

# print('saved to db')
teardown_method(driver)


 
