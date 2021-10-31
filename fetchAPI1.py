import requests
textFile = 'data/cached-responses/test.xml'
url="http://portalquery.just.ro/Query.asmx?WSDL"
#headers = {'content-type': 'application/soap+xml'}
headers = {'content-type': 'text/xml'}
body = """<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <CautareDosare xmlns="portalquery.just.ro">
      <institutie>CurteadeApelBUCURESTI</institutie>
      <dataStart>2021-05-27</dataStart>
      <dataStop>2021-05-28</dataStop>
    </CautareDosare>
  </soap12:Body>
</soap12:Envelope>
"""

response = requests.post(url,data=body,headers=headers)
# print(response.content)
ztring = response.content.decode("utf-8")
with open(textFile, "w") as text_file:
    text_file.write(ztring)

print('done')