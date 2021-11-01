import xmltodict
import gzip
import json
from icecream import ic
import pandas as pd
import sqlite3
import glob, os
import pandas as pd

dbfile = "data/portal-just.db"
csvinstante ="data/reference/instante.csv"
dir_xmlgz = 'data/cached-responses/xmlgz/'
dir_parsed = 'data/cached-responses/parsed/'

instante = pd.read_csv (csvinstante)

def qiDosar(ddosar, xid): 

  if not ddosar['numarVechi']:
    ddosar['numarVechi'] = ''

  try:
    sqlq = "INSERT INTO Dosar (xnr, numar, \"Numar vechi\", data, institutie, categorieCaz, stadiuProcesual, parti, sedinte, caiAtac) VALUES (\"" + str(xid) + "\",\"" + str(xid) + "\",\"" + str(xid) + "\",\"" + ddosar['data'] + "\",\"" + ddosar['institutie'] + "\",\"" + ddosar['categorieCaz'] + "\",\"" + ddosar['stadiuProcesual'] + "\",\"" + '[listă]' + "\",\"" + '[listă]' + "\",\"" + '[listă]' +  "\")"
  except:
    print('err: qiDosar no sqlq')
    breakpoint()
  return sqlq
 
def qiDosarParte(ddosar, xid): 
  values = ''
  sqlstart = 'INSERT INTO DosarParte (xnumardosar, nume, calitateParte) '

  parti = ddosar['parti']['DosarParte']

  if type(parti) is list:
    # mai multe părți:
    for oparte in parti:
      try:
        values += "(\"" + str(xid) + "\",\"" + oparte['nume'].replace('"','""') + "\",\"" + oparte['calitateParte'] + "\"), "
      except:
        print('no parti')
        print(ddosar['parti'])
        breakpoint()
    values = values[:-2] + ';'
  else:
    # o singură parte:  
    values += "(\"" + str(xid) + "\",\"" + parti['nume'].replace('"','""') + "\",\"" + parti['calitateParte'] + "\"); "
    
  return (sqlstart + 'VALUES ' + values)
 
def xmltodb(inputxmlz, xdbfile):
  conn = sqlite3.connect(xdbfile)
  cursor = conn.cursor()
  zz = xmltodict.parse(gzip.GzipFile(inputxmlz))
  # print(json.dumps(zz))
  zecsv=[]
  dosare = zz["soap:Envelope"]['soap:Body']["CautareDosareResponse"]["CautareDosareResult"]['Dosar']
  for dosar in dosare:
    instanta = instante.loc[instante['api-slug'] == dosar['institutie']]

    try:
      linkpjr = str(int(float(instanta['link just-ro'])))
    except: 
      linkpjr = ''

    try:
      znr = instanta['tip']+'x'+linkpjr+'_'+dosar['numar']
      xnr = znr.iloc[0] #gets data from df
    except:
      print('ERR: failed at xnr zrn')
      breakpoint()
 
    # TODO: add relational tables: parti, sedinte, caiatac
    # write dosar, DosarParte, DosarSedinta, DosarCaleAtac 
 
    sqlDosar = qiDosar(dosar, xnr)
    try:
      cursor.execute(sqlDosar)
    except sqlite3.Error as err:
        print('--err sqlDosar Query Failed: %s\nError: %s' % (sqlDosar, str(err)))
        breakpoint()
    if 'parti' in dosar:
      sqlDosarParte = qiDosarParte(dosar, xnr)
      try:
        cursor.execute(sqlDosarParte)
      except sqlite3.Error as err:
          print('--err sqlDosarParte Query Failed: %s\nError: %s' % (sqlDosarParte, str(err)))
          breakpoint()
      
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