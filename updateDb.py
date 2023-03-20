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

debugging = False

instante = pd.read_csv (csvinstante)

def qiDosar(ddosar, xid): 
  # breakpoint()
  if 'numarVechi' not in ddosar or not ddosar['numarVechi']:
    ddosar['numarVechi'] = ''
  if not ddosar['data']:
    ddosar['data'] = ''
  if not ddosar['institutie']:
    ddosar['institutie'] = ''
  if not ddosar['categorieCaz']:
    ddosar['categorieCaz'] = ''
  if not ddosar['stadiuProcesual']:
    ddosar['stadiuProcesual'] = ''

  # try:
  #   parti = json.dumps(ddosar['parti']['DosarParte'])
  # except:
  #   parti = ''
  
  # try:
  #   sedinte = json.dumps(ddosar['sedinte']['DosarSedinta'])
  # except:
  #   sedinte = ''
  
  # try:
  #   caiAtac = json.dumps(ddosar['caiAtac']['DosarCaleAtac'])
  # except:
  #   caiAtac = ''
  
  # try:

  #   # sqlq = "INSERT INTO Dosar (xnr, numar, \"Numar vechi\", data, institutie, categorieCaz, stadiuProcesual, parti, sedinte, caiAtac) VALUES (\"" + str(xid) + "\",\"" + ddosar['numar'] + "\",\"" + ddosar['numarVechi'] + "\",\"" + ddosar['data'] + "\",\"" + ddosar['institutie'] + "\",\"" + ddosar['categorieCaz'] + "\",\"" + ddosar['stadiuProcesual'] + "\",\"" + parti + "\",\"" + sedinte + "\",\"" + caiAtac +  "\")"
  #   # sqlq = "INSERT INTO Dosar (xnr, numar, \"Numar vechi\", data, institutie, categorieCaz, stadiuProcesual) VALUES (\"" + str(xid) + "\",\"" + ddosar['numar'] + "\",\"" + ddosar['numarVechi'] + "\",\"" + ddosar['data'] + "\",\"" + ddosar['institutie'] + "\",\"" + ddosar['categorieCaz'] + "\",\"" + ddosar['stadiuProcesual'] + "\")"
  fields = ('xnr', 'numar', '\"Numar vechi\"', 'data', 'institutie', 'categorieCaz', 'stadiuProcesual', 'parti', 'sedinte', 'caiAtac')
  sqlTemplate = "INSERT INTO Dosar (xnr, numar, \"Numar vechi\", data, institutie, categorieCaz, stadiuProcesual) VALUES (?, ?, ?, ?, ?, ?, ?)"
  data = (str(xid), ddosar['numar'], ddosar['numarVechi'], ddosar['data'], ddosar['institutie'], ddosar['categorieCaz'], ddosar['stadiuProcesual'])
    
  # except:
  #   print('err: qiDosar no sqlq')
  #   if debugging:
  #     breakpoint()
  
  return {"sqlTemplate": sqlTemplate, "values": data}
 
def qiDosarParte(ddosar, xid): 
  values = ()
  fields = ('xnumardosar', 'nume', 'calitateParte')
  sqlTemplate = 'INSERT INTO DosarParte (xnumardosar, nume, calitateParte) VALUES (?, ?, ?)'
  parti = ddosar['parti']['DosarParte']

  if type(parti) is list:
    # mai multe părți:
    for oparte in parti:
      try:
        # values += "(\"" + str(xid) + "\",\"" + oparte['nume'].replace('"','""') + "\",\"" + oparte['calitateParte'] + "\"), "
        values += (xid, parti['nume'].replace('"','""').replace("'", "\\'"), parti['calitateParte'])
      except:
        print('no parti')
        # print(ddosar['parti'])
        if debugging:
          breakpoint()
    # values = values[:-2] + ';'
  else:
    # o singură parte:  
    # values += "(\"" + str(xid) + "\",\"" + parti['nume'].replace('"','""') + "\",\"" + parti['calitateParte'] + "\"); "
    # values += (xid, parti['nume'].replace('"','""').replace("'", "\\'"), parti['calitateParte'])
    values += (xid, parti['nume'].replace("'", "\\'"), parti['calitateParte'])
    
  # return {"fields": fields, "values": values}
  return {"sqlTemplate": sqlTemplate, "values": values}

def qiDosarSedinta(ddosar, xid): 
  values = ()
  # fields = ('xnumardosar', 'complet', 'data', 'ora', 'soluţie', 'soluţieSumar', 'dataPronuntare', 'documentSedinta', 'numarDocument', 'dataDocument')
  sqlTemplate = 'INSERT INTO DosarSedinta (xnumardosar, complet, data, ora, soluţie, soluţieSumar, dataPronuntare, documentSedinta, numarDocument, dataDocument) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
  sedinte = ddosar['sedinte']['DosarSedinta']

  if type(sedinte) is list:
    # mai multe părți:
    for osedinta in sedinte:
      osedinta['documentSedinta'] = 'xx'
      if (osedinta['numarDocument'] is None):
        osedinta['numarDocument'] = ''
      if (osedinta['solutie'] is None):
        osedinta['solutie'] = ''
      if (osedinta['solutieSumar'] is None):
        osedinta['solutieSumar'] = ''
      try:
        values += (xid,  osedinta['complet'], osedinta['data'], osedinta['ora'], osedinta['solutie'], osedinta['solutieSumar'].replace("'", "\\'"), osedinta['dataPronuntare'], osedinta['documentSedinta'], osedinta['numarDocument'], osedinta['dataDocument'])
      except:
        print('err 101: no sedinte ' + xid)
        # print(ddosar['sedinte'])
        if debugging:
          breakpoint()
    # values = values[:-2] + ';'
  else:
    # o singură parte:
    # FIXME:
    if not isinstance(sedinte['dataPronuntare'], str):
      sedinte['dataPronuntare'] = 'rr'
    if sedinte['numarDocument'] is None:
      sedinte['numarDocument'] = ''
    if sedinte['solutie'] is None:
      sedinte['solutie'] = ''
    if sedinte['solutieSumar'] is None:
      sedinte['solutieSumar'] = ''

    try:  
      values += (xid ,   sedinte['complet'] , sedinte['data'] , sedinte['ora'] , sedinte['solutie'] , sedinte['solutieSumar'] , sedinte['dataPronuntare'] , sedinte['documentSedinta'] , sedinte['numarDocument'] , sedinte['dataDocument'])
    except:
      print('--err values osedinta')
      if debugging:
        breakpoint()
    
  return {"sqlTemplate": sqlTemplate, "values": values}
 
def xmltodb(inputxmlz, xdbfile):
  conn = sqlite3.connect(xdbfile)
  cursor = conn.cursor()
  try:
    zz = xmltodict.parse(gzip.GzipFile(inputxmlz))
  except:
    print('ERR 114: ' + inputxmlz)
    return None
  # print(json.dumps(zz))
  zecsv=[]
  # breakpoint()
  
  #FIXME: check if ["CautareDosareResult"]['Dosar'] exist
  dosare = zz["soap:Envelope"]['soap:Body']["CautareDosareResponse"]["CautareDosareResult"]['Dosar']
  for dosar in dosare:
    
    if 'institutie' in dosar:
      # print(dosar['institutie'])
      instanta = instante.loc[instante['api-slug'] == dosar['institutie']]
    else:
      # print('wtf')
      # breakpoint()
      instanta = '-na-'

    try:
      linkpjr = str(int(float(instanta['link just-ro'])))
    except: 
      linkpjr = ''

    try:
      znr = instanta['tip']+'-'+linkpjr+'_'+dosar['numar']
      xnr = znr.iloc[0] #gets data from df
    except:
      print('ERR 143: failed at xnr zrn' + inputxmlz)
      xnr = 'xx-zz'
      znr = 'yy-zz'
      return None

      if debugging:
        breakpoint()
 
    # TODO: add relational tables: parti, sedinte, caiatac
    # write dosar, DosarParte, DosarSedinta, DosarCaleAtac 
  
    xsql = qiDosar(dosar, xnr)
    try:
      cursor.execute(xsql['sqlTemplate'], xsql['values'])
    except sqlite3.Error as err:
        print('Err 158 ' + inputxmlz + 'sqlDosar Query Failed: %s\nError: %s' % (xsql['values'], str(err)))
        breakpoint()
        if debugging:
          breakpoint()

    if 'parti' in dosar:
      xsqlDosarParte = qiDosarParte(dosar, xnr)
      try:
        cursor.execute(xsqlDosarParte['sqlTemplate'], xsqlDosarParte['values'])
      except sqlite3.Error as err:
          print('err 167 ' + inputxmlz + ' sqlDosarParte Query Failed: %s\nError: %s' % (xsqlDosarParte['values'], str(err)))
          breakpoint()
          if debugging:
            breakpoint()
    
    if 'sedinte' in dosar:
      xsqlDosarSedinta = qiDosarSedinta(dosar, xnr)
      try:
        cursor.execute(xsqlDosarSedinta['sqlTemplate'], xsqlDosarSedinta['values'])
      except sqlite3.Error as err:
          print('err 176 ' + inputxmlz + ' sqlDosarSedinta Query Failed: %s\nError: %s' % (xsqlDosarSedinta['values'], str(err)))

          if debugging:
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