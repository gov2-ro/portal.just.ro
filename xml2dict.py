import xmltodict
import gzip
import json
from icecream import ic
import pandas as pd
import sqlite3

inputxml = 'data/cached-responses/test.xml'
inputxmlz = 'data/cached-responses/test.xml.gz'
outputjson = 'data/json-responses/test.json'
dbfile = "data/portal-just.db"

conn = sqlite3.connect(dbfile)
cursor = conn.cursor()

zz = xmltodict.parse(gzip.GzipFile(inputxmlz))
# print(json.dumps(zz))

# (Pdb) print(zz["soap:Envelope"]['soap:Body']["CautareDosareResponse"]["CautareDosareResult"]['Dosar'][0]['numar'])
zecsv=[]
dosare = zz["soap:Envelope"]['soap:Body']["CautareDosareResponse"]["CautareDosareResult"]['Dosar']
for dosar in dosare:
  ddosar = dosar
 
  # if 'parti' in dosar:
  #   ddosar['parti'] = str(dosar['parti']) 
  # else:
  #   ddosar['parti'] = '--'
  
  # if 'sedinte' in dosar:
  #   ddosar['sedinte'] = str(dosar['sedinte']) 
  # else:
  #   ddosar['sedinte'] = '--'
  
  # if 'caiAtac' in dosar:
  #   ddosar['caiAtac'] = str(dosar['caiAtac']) 
  # else:
  #   ddosar['caiAtac'] = '--'
  ddosar['parti'] = 'xx'
  ddosar['sedinte'] = 'xx'
  ddosar['caiAtac'] = 'xx'
  ddosar['numarVechi'] = dosar['numarVechi'] if dosar['numarVechi'] else '--'
  try:
    xx = ",".join(ddosar.values())
  except:
    print('no join')
    ic(ddosar)
  
  sqlq = "INSERT INTO Dosar (numar, \"Numar vechi\", data, institutie, categorieCaz, stadiuProcesual, parti, sedinte, caiAtac) VALUES (\"" + ddosar['numar'] + "\",\"" + ddosar['numarVechi'] + "\",\"" + ddosar['data'] + "\",\"" + ddosar['institutie'] + "\",\"" + ddosar['categorieCaz'] + "\",\"" + ddosar['stadiuProcesual'] + "\",\"" + ddosar['parti'] + "\",\"" + ddosar['sedinte'] + "\",\"" + ddosar['caiAtac'] +  "\")"
  
  # breakpoint()
  cursor.execute(sqlq)


conn.commit()

print('done')
# with open(outputjson, 'w') as outfile:
#      json.dump(zz, outfile, sort_keys = True, indent = 4,
#                ensure_ascii = False)