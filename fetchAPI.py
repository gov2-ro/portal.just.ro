import requests, os, datetime, random, time, csv
import gzip
import xml.etree.ElementTree as ET

start_date = datetime.date(2020, 7, 16)
end_date = datetime.date(2021, 12, 30)

logcsv = 'data/cached-responses/log.csv'
dir_responsexml = 'data/cached-responses/xml/'
dir_responsexmlgz = 'data/cached-responses/xmlgz/'
url="http://portalquery.just.ro/Query.asmx?WSDL"
#headers = {'content-type': 'application/soap+xml'}
headers = {'content-type': 'text/xml'}
#TODO: loop or add all Instanțe or just ignore

# cautaDosar <date:yyyy-mm-dd mandatory> <days=1> <direction=back> 
def cautaDosarXMLQ(date, *opts):
  if not opts:
    dateStart = date + 'T00:00:00Z'
    dateEnd = date + 'T23:59:59Z'
  # TODO: check direction
  else:
    dateStart = date + 'T00:00:00Z'
    # TODO: smartly traverse dates 31 + 1 = 1 m+1 

  qbody = """<?xml version="1.0" encoding="utf-8"?>
  <soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
      <CautareDosare xmlns="portalquery.just.ro">
        <dataStart>{dataStart}</dataStart>
        <dataStop>{dataStop}</dataStop>
      </CautareDosare>
    </soap12:Body>
  </soap12:Envelope>
  """.format(dataStart = dateStart, dataStop = dateEnd)
  # print(qbody)
  # breakpoint()()
  return qbody

def api2xml(zidate, body):
  response = requests.post(url,data=body,headers=headers)
  ztring = response.content.decode("utf-8")
  num_dosars = None
  min_dosar_date = None
  max_dosar_date = None
  # convert to xml obj to count nr of dosare?
  try:
    xtree = ET.ElementTree(ET.fromstring(ztring))
    root = xtree.getroot()
    nrdosare = 0

    for dosar in root.findall('.//{portalquery.just.ro}Dosar'):
      nrdosare += 1
    dosar_nodes = root.findall('.//{portalquery.just.ro}Dosar')
    num_dosars = len(dosar_nodes)
    # print(str(nrdosare) + ' ' + str(num_dosars))

# get min max date
    for dosar_node in root.findall('.//{portalquery.just.ro}Dosar'):    
      dosar_date_str = dosar_node.find("./{portalquery.just.ro}data").text
      dosar_date = datetime.datetime.strptime(dosar_date_str, '%Y-%m-%dT%H:%M:%S')
      if min_dosar_date is None or dosar_date < min_dosar_date:
          min_dosar_date = dosar_date
      if max_dosar_date is None or dosar_date > max_dosar_date:
          max_dosar_date = dosar_date
  
    if nrdosare == 0:
      return None
  except:
    nrdosare = 600666006
  # Write results to CSV file
  with open(logcsv, mode='a', newline='') as csvfile:
      writer = csv.writer(csvfile)
      writer.writerow([zidate, nrdosare, num_dosars, min_dosar_date, max_dosar_date])

  iyear, imonth = map(int, zidate.split('-')[0:2])
  year = str(iyear)
  month = str(imonth)

  if not os.path.exists(dir_responsexml + year):
    os.makedirs(dir_responsexml + year)
    time.sleep(random.randint(0, 7))
  if not os.path.exists(dir_responsexml + year + '/' + month):
    os.makedirs(dir_responsexml + year + '/' + month)
    time.sleep(random.randint(0, 2))

  with open(dir_responsexml + year + '/' + month + '/' + zidate + ' ' + str(nrdosare) + ' dosare.xml', "w") as text_file:
      text_file.write(ztring)
  print('>> ' + dir_responsexml + year + '/' + month + zidate + '_dosare.xml')

  # with gzip.open(dir_responsexmlgz + year + '/' + zidate + '_dosare.xml.gz', 'wt') as f:
  #   f.write(ztring)
  # print('- saved: ' + dir_responsexmlgz + zidate + '_dosare.xml.gz')

# TODO: this should happen in external script - or not.

# dates = ['2022-02-10', '2023-01-11', '2023-02-12']

# loop over all dates between start and end dates
dates = []
current_date = start_date
while current_date <= end_date:
    # append current date to list in yyyy-mm-dd format
    dates.append(current_date.strftime('%Y-%m-%d'))
    # increment current date by 1 day
    current_date += datetime.timedelta(days=1)


# TODO: if file xml exists don't fetch!

for oneday in dates:
  filename=oneday
  # print('>> fetching Dosare date: ' + oneday + ' ...')
  api2xml(oneday, cautaDosarXMLQ(oneday))
  # print('-- fetched Dosare date: ' + oneday)
  print('-- ' + oneday)
  # time.sleep(random.randint(0, 3))