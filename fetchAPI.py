import requests
import gzip

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
  # breakpoint()
  return qbody

def api2xml(target, body):
  response = requests.post(url,data=body,headers=headers)
  ztring = response.content.decode("utf-8")
  
  with open(dir_responsexml + target + '_dosare.xml', "w") as text_file:
      text_file.write(ztring)
  print('- saved: ' + dir_responsexml + target + '_dosare.xml')

  with gzip.open(dir_responsexmlgz + target + '_dosare.xml.gz', 'wt') as f:
    f.write(ztring)
  print('- saved: ' + dir_responsexmlgz + target + '_dosare.xml.gz')

# TODO: this should happen in external script

dates = ['2021-05-28', '2021-05-29', '2021-05-30']

# TODO: if file xml exists don't fetch!

for oneday in dates:
  filename=oneday
  print('>> fetching Dosare date: ' + oneday + ' ...')
  api2xml(oneday, cautaDosarXMLQ(oneday))
  print('-- fetched Dosare date: ' + oneday)
