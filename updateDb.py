import xmltodict
import gzip
import json
from icecream import ic
import pandas as pd
import sqlite3
import glob, os
import pandas as pd
import csv
import logging

dbfile = "data/portal-just.db"
csvinstante ="data/reference/instante.csv"
dir_xmlgz = 'data/cached-responses/xmlgz/'
dir_parsed = 'data/cached-responses/parsed/'
errLogFile = 'data/errz.csv'
errBuffer = 50 #save errors at each errBuffer counted
debugging = False

errz = [['err code', 'fisier', 'xnr dosar','eroare', 'extra']]
errCount = 0
instante = pd.read_csv (csvinstante)


def qiDosar(ddosar, xid, fisier): 
  global errCount
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

  try:
    sqlq = "INSERT INTO Dosar (xnr, numar, \"Numar vechi\", data, institutie, categorieCaz, stadiuProcesual) VALUES (\"" + xid + "\",\"" + ddosar['numar'] + "\",\"" + ddosar['numarVechi'] + "\",\"" + ddosar['data'] + "\",\"" + ddosar['institutie'] + "\",\"" + ddosar['categorieCaz'] + "\",\"" + ddosar['stadiuProcesual'] + "\")"
  except Exception as e:
    # print('err: qiDosar no sqlq')
    errz.append(['47 qiDosar no sqlq',fisier,xid,str(e),''])
    errCount += 1
    if debugging:
      breakpoint()
  return sqlq
 

def qiDosarParte(ddosar, xid, fisier): 
  global errCount
  values = ''
  sqlstart = 'INSERT INTO DosarParte (xnumardosar, nume, calitateParte) '
  parti = ddosar['parti']['DosarParte']

  if type(parti) is list:
    # mai multe părți:
    for oparte in parti:
      if 'nume' not in oparte or oparte['nume'] == '':
        oparte['nume'] = ''
      try:
        values += "(\"" + str(xid) + "\",\"" + oparte['nume'].replace('"','""') + "\",\"" + oparte['calitateParte'].replace('"','""') + "\"), "
      except Exception as e:
        # print('no parti')
        errz.append(['66 qiDosarParte no părți',fisier,xid,str(e),''])
        errCount += 1
        if debugging:
          breakpoint()
    values = values[:-2] + ';'
  else:
    # o singură parte:  
    values += "(\"" + str(xid) + "\",\"" + parti['nume'].replace('"','""') + "\",\"" + parti['calitateParte'].replace('"','""') + "\"); "
    
  return (sqlstart + 'VALUES ' + values)


def qiDosarSedinta(ddosar, xid, fisier): 
  global errCount
  values = ''
  sqlstart = 'INSERT INTO DosarSedinta (xnumardosar, complet, data, ora, soluţie, soluţieSumar, dataPronuntare, documentSedinta, numarDocument, dataDocument) '

  sedinte = ddosar['sedinte']['DosarSedinta']

  if type(sedinte) is list:
    # mai multe părți:
    for osedinta in sedinte:
      if (osedinta['complet'] is None):
        osedinta['complet'] = ''
      if (osedinta['documentSedinta'] is None):
        osedinta['documentSedinta'] = 'xx'
      if (osedinta['numarDocument'] is None):
        osedinta['numarDocument'] = 'xx'
      if (osedinta['solutie'] is None):
        osedinta['solutie'] = 'xx'
      if (osedinta['solutieSumar'] is None):
        osedinta['solutieSumar'] = 'xx'
      if isinstance(osedinta['dataDocument'] , dict):
        osedinta['dataDocument'] = '-na-NIL'
      if isinstance(osedinta['dataPronuntare'] , dict):
        osedinta['dataPronuntare'] = '-na-NIL'
      if isinstance(osedinta['documentSedinta'] , dict):
        osedinta['documentSedinta'] = '-na-NIL'
      try:
        values += "(\"" + str(xid) + "\",\"" +  osedinta['complet'] + "\",\"" + osedinta['data'] + "\",\"" + osedinta['ora'] + "\",\"" + osedinta['solutie'].replace('"','""') + "\",\"" + osedinta['solutieSumar'].replace('"','""') + "\",\"" + osedinta['dataPronuntare'] + "\",\"" + osedinta['documentSedinta'] + "\",\"" + osedinta['numarDocument'] + "\",\"" + osedinta['dataDocument'] + "\"), "
      except Exception as e:
        # print('warning 84: no sedinte ' + xid + ' ' + fisier + ' :: ' +str(e))
        errz.append(['105 qiDosarSedinta no ședințe',fisier,xid,str(e),''])
        errCount += 1
        breakpoint()
        # print(ddosar['sedinte'])
        if debugging:
          breakpoint()
    values = values[:-2] + ';'
  else:
    # o singură parte:
    # FIXME:
    if not isinstance(sedinte['dataPronuntare'], str):
      sedinte['dataPronuntare'] = '-na-'
    if sedinte['numarDocument'] is None:
      sedinte['numarDocument'] = '-na-'
    if sedinte['complet'] is None:
      sedinte['complet'] = '-na-'
    if sedinte['solutie'] is None:
      sedinte['solutie'] = '-na-'
    if sedinte['solutieSumar'] is None:
      sedinte['solutieSumar'] = '-na-'
    if isinstance(sedinte['dataDocument'] , dict):
        sedinte['dataDocument'] = '-na-NIL'
    if isinstance(sedinte['dataPronuntare'] , dict):
        sedinte['dataPronuntare'] = '-na-NIL'
    if isinstance(sedinte['documentSedinta'] , dict):
        sedinte['documentSedinta'] = '-na-NIL'
    try:  
      values += "(\"" + str(xid) + "\",\"" +   sedinte['complet'] + "\",\"" + sedinte['data'] + "\",\"" + sedinte['ora'] + "\",\"" + sedinte['solutie'].replace('"','""') + "\",\"" + sedinte['solutieSumar'].replace('"','""') + "\",\"" + sedinte['dataPronuntare'] + "\",\"" + sedinte['documentSedinta'] + "\",\"" + sedinte['numarDocument'] + "\",\"" + sedinte['dataDocument'] + "\"); "
    except Exception as e:
      # print('err 118 values osedinta: ' + str(e))
      errz.append(['135 qiDosarSedinta oSedinta?',fisier,xid,str(e),''])
      errCount += 1
      breakpoint()

      if debugging:
        breakpoint()
  if not values:
    return None  
  else:
    return (sqlstart + 'VALUES ' + values)


def qiDosarCaiAtac(ddosar, xid, fisier):
  global errCount
  values = ''
  sqlstart = 'INSERT INTO DosarCaleAtac (xnumardosar, dataDeclarare, parteDeclaratoare, tipCaleAtac) '
  caleAtac = ddosar['caiAtac']['DosarCaleAtac']
  if type(caleAtac) is list:
  # mai multe părți:
    for oCale in caleAtac:
      if oCale['parteDeclaratoare'] is None:
        oCale['parteDeclaratoare'] = '-na-'
      try:
        values += "(\"" + str(xid) + "\",\"" + oCale['dataDeclarare'] + "\",\"" + oCale['parteDeclaratoare'].replace('"','""') + "\",\"" + oCale['tipCaleAtac'] + "\"), "
      except Exception as e:
        # print('warning 143 no caleAtac ' + xid + ' --> ' + fisier)
        errz.append(['161 qiDosarCaiAtac no caleAtac',fisier,xid,str(e),''])
        errCount += 1
        # print(ddosar['caleAtac'])
        if debugging:
          breakpoint()
    values = values[:-2] + ';'
  else:
    # o singură parte:  
    if caleAtac['parteDeclaratoare'] is None:
      caleAtac['parteDeclaratoare'] = '-na-'
    try:
      values += "(\"" + str(xid) + "\",\"" + caleAtac['dataDeclarare'] + "\",\"" + caleAtac['parteDeclaratoare'].replace('"','""') + "\",\"" + caleAtac['tipCaleAtac'] + "\"); "
    except Exception as e:
      # print('err 154: căi atac ' + xid + ' ' + fisier + ' :: ' +str(e))
      errz.append(['175 qiDosarCaiAtac',fisier,xid,str(e),''])
      errCount += 1
      if debugging:
        breakpoint()
      return None
        
  return (sqlstart + 'VALUES ' + values)


def xmltodb(inputxmlz, xdbfile):
  global errCount
  conn = sqlite3.connect(xdbfile)
  cursor = conn.cursor()
  try:  
    zz = xmltodict.parse(gzip.GzipFile(inputxmlz))
  except Exception as e:
    # print('err 185 xmltodict.parse(gzip.GzipFile' + inputxmlz)
    errz.append(['192 xmltodb xmltodict.parsegzip',inputxmlz,'',str(e),''])
    errCount += 1
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
      instanta = '-nax-'
    

    try:
      linkpjr = str(int(float(instanta['link just-ro'])))
    except: 
      linkpjr = '--na--'
    
 

    if 'tip' not in instanta:
        
        errz.append(['221 xmltodb failed instanta[\'tip\']',inputxmlz,'','',''])
        errCount += 1
        return None

    if isinstance(instanta['tip'],  pd.DataFrame):
        errz.append(['226 xmltodb failed instanta[\'tip\']',inputxmlz,dosar['numar'],'',''])
        errCount += 1
        instanta['tip'] = '-n2-'

    try:
      znr = instanta['tip']+'-'+linkpjr+'_'+dosar['numar']
    except Exception as e:
      breakpoint()
      errz.append(['220 xmltodb failed at zrn',inputxmlz,dosar['numar'],str(e),''])
      errCount += 1
      return None

    if isinstance(znr , dict):
      errz.append(['227 xmltodb zrn is dict?!',inputxmlz,dosar['numar'],str(e),json.dumps(znr)])
      errCount += 1
      return None

    if isinstance(znr,  pd.Series):
      errz.append(['240 xmltodb zrn is panda series',inputxmlz,dosar['numar'],'zrn is pd.Series',znr.to_string()])
      errCount += 1
      return None

    try:
      xnr = znr.iloc[0] #gets data from df
    except Exception as e:
      breakpoint()
      # print('ERR 141: failed at xnr zrn ' + inputxmlz + ' --> '+ str(e))
      errz.append(['249 xmltodb failed at xnr',inputxmlz,znr,str(e),instanta['tip'] + "\n\r" +linkpjr + "\n\r" + dosar['numar']])
      errCount += 1
      return None
  
    sqlDosar = qiDosar(dosar, xnr, inputxmlz)

    try:
      cursor.execute(sqlDosar)
    except sqlite3.Error as err:
        # print('err 158 sqlDosar Query Failed: %s\nError: %s' % (sqlDosar, str(err)))
        errz.append(['239 sqlDosar Query Fail',inputxmlz,dosar['numar'], str(err),sqlDosar])
        errCount += 1
        if debugging:
          breakpoint()

    if 'parti' in dosar:
      sqlDosarParte = qiDosarParte(dosar, xnr, inputxmlz)
      try:
        cursor.execute(sqlDosarParte)
      except sqlite3.Error as err:
          # print('err 241 sqlDosarParte Query Failed: %s\nError: %s' % (sqlDosarParte, str(err)) + ' --> ' + inputxmlz)
          errz.append(['242 sqlDosarParte Query Fail',inputxmlz,xnr, str(err),sqlDosarParte])
          errCount += 1
          if debugging:
            breakpoint()
    
    if 'sedinte' in dosar:
      sqlDosarSedinta = qiDosarSedinta(dosar, xnr, inputxmlz)
      if sqlDosarSedinta:
        try:
          cursor.execute(sqlDosarSedinta)
        except sqlite3.Error as err:
            # print('--err sqlDosarSedinta Query Failed: %s\nError: %s' % (sqlDosarSedinta, str(err)))
            errz.append(['262 sqlDosarSedinta Query Fail',inputxmlz,xnr, str(err),sqlDosarSedinta])
            errCount += 1
            if debugging:
              breakpoint()

    if 'caiAtac' in dosar:
      sqlCaleAtac = qiDosarCaiAtac(dosar, xnr, inputxmlz)
      if sqlCaleAtac:
        try:
          cursor.execute(sqlCaleAtac)
        except sqlite3.Error as err:
          # print('err 242 sqlCaleAtac Query Failed: %s\nError: %s' % (sqlCaleAtac, str(err)) + ' --> ' + xnr)
          errz.append(['264 sqlCaleAtac Query Fail',inputxmlz,xnr, str(err),sqlCaleAtac])
          errCount += 1

  conn.commit()
  print('--> ' + inputxmlz) 


# loop all files in xmlgz, writhe to sqlite, move file

filez = [os.path.basename(x) for x in glob.glob(dir_xmlgz + "*.xml.gz")]
 
for file in filez:
  print('reading ' + dir_xmlgz + file)
  xmltodb(dir_xmlgz + file, dbfile)

  # each errBuffer errors, save to file
  if errCount >= errBuffer:
    # Open the CSV file in write mode
    with open(errLogFile, mode='a', newline='') as errFile:

        # Create a CSV writer object
        writer = csv.writer(errFile)

        # Write each row of the list of lists to the CSV file
        for row in errz:
            writer.writerow(row)
        print ('-------- saved ' + str(errBuffer) + ' more errors')
    errCount = 0
    errz = []
  
  # move file
  os.rename(dir_xmlgz + file, dir_parsed + file)
  print('written to sql: ' + file)

print('>> DONE')