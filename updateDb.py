import xmltodict
import gzip
import json
from icecream import ic
import pandas as pd
import sqlite3
import glob, os

dbfile = "data/portal-just.db"
dir_xmlgz = 'data/cached-responses/xmlgz/'
dir_parsed = 'data/cached-responses/parsed/'

def xmltodb(inputxmlz, xdbfile):
  conn = sqlite3.connect(xdbfile)
  cursor = conn.cursor()
  zz = xmltodict.parse(gzip.GzipFile(inputxmlz))
  # print(json.dumps(zz))
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
    ddosar['xnr'] = dosar['institutie']+'_'+dosar['numar']
    ddosar['parti'] = 'xx'
    ddosar['sedinte'] = 'xx'
    ddosar['caiAtac'] = 'xx'
    ddosar['numarVechi'] = dosar['numarVechi'] if dosar['numarVechi'] else '--'
    try:
      xx = ",".join(ddosar.values())
    except:
      print('no join')
      ic(ddosar)
    
    sqlq = "INSERT INTO Dosar (xnr, numar, \"Numar vechi\", data, institutie, categorieCaz, stadiuProcesual, parti, sedinte, caiAtac) VALUES (\"" + ddosar['xnr'] + "\",\"" + ddosar['numar'] + "\",\"" + ddosar['numarVechi'] + "\",\"" + ddosar['data'] + "\",\"" + ddosar['institutie'] + "\",\"" + ddosar['categorieCaz'] + "\",\"" + ddosar['stadiuProcesual'] + "\",\"" + ddosar['parti'] + "\",\"" + ddosar['sedinte'] + "\",\"" + ddosar['caiAtac'] +  "\")"
    
    # TODO: add relational tables: parti, sedinte, caiatac
    cursor.execute(sqlq)

  conn.commit()
  print('witten: ' + inputxmlz) 

# loop all files in xmlgz, writhe to sqlite, move file

filez = [os.path.basename(x) for x in glob.glob(dir_xmlgz + "*.xml.gz")]
 
for file in filez:
  print('reading ' + dir_xmlgz + file)
  xmltodb(dir_xmlgz + file, dbfile)
  
  # move file
  os.rename(dir_xmlgz + file, dir_parsed + file)

  print('written to sql: ' + file)

print('>> DONE')