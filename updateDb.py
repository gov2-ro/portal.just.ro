import xmltodict
import gzip
import json
from icecream import ic
import pandas as pd
import sqlite3
import glob, os
import pandas as pd
import logging

dbfile = "data/portal-just.db"
csvinstante ="data/reference/instante.csv"
dir_xmlgz = 'data/cached-responses/xmlgz/'
dir_parsed = 'data/cached-responses/parsed/'

debugging = False

instante = pd.read_csv (csvinstante)

#TODO: add logging and error logging

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

  try:
    sqlq = "INSERT INTO Dosar (xnr, numar, \"Numar vechi\", data, institutie, categorieCaz, stadiuProcesual) VALUES (\"" + xid + "\",\"" + ddosar['numar'] + "\",\"" + ddosar['numarVechi'] + "\",\"" + ddosar['data'] + "\",\"" + ddosar['institutie'] + "\",\"" + ddosar['categorieCaz'] + "\",\"" + ddosar['stadiuProcesual'] + "\")"
  except:
    print('err: qiDosar no sqlq')
    if debugging:
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
        # print(ddosar['parti'])
        if debugging:
          breakpoint()
    values = values[:-2] + ';'
  else:
    # o singură parte:  
    values += "(\"" + str(xid) + "\",\"" + parti['nume'].replace('"','""') + "\",\"" + parti['calitateParte'] + "\"); "
    
  return (sqlstart + 'VALUES ' + values)


def qiDosarSedinta(ddosar, xid, fisier): 
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
        print('warning 84: no sedinte ' + xid + ' ' + fisier + ' :: ' +str(e))
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
      values += "(\"" + str(xid) + "\",\"" +   sedinte['complet'] + "\",\"" + sedinte['data'] + "\",\"" + sedinte['ora'] + "\",\"" + sedinte['solutie'] + "\",\"" + sedinte['solutieSumar'] + "\",\"" + sedinte['dataPronuntare'] + "\",\"" + sedinte['documentSedinta'] + "\",\"" + sedinte['numarDocument'] + "\",\"" + sedinte['dataDocument'] + "\"); "
    except Exception as e:
      print('err 118 values osedinta: ' + str(e))
      breakpoint()

      if debugging:
        breakpoint()
  if not values:
    return None  
  else:
    return (sqlstart + 'VALUES ' + values)


def qiDosarCaiAtac(ddosar, xid, fisier):
  values = ''
  sqlstart = 'INSERT INTO DosarCaleAtac (xnumardosar, dataDeclarare, parteDeclaratoare, tipCaleAtac) '
  caleAtac = ddosar['caiAtac']['DosarCaleAtac']
  if type(caleAtac) is list:
  # mai multe părți:
    for oCale in caleAtac:
      try:
        values += "(\"" + str(xid) + "\",\"" + oCale['dataDeclarare'] + "\",\"" + oCale['parteDeclaratoare'].replace('"','""') + "\",\"" + oCale['tipCaleAtac'] + "\"), "
      except:
        print('warning 143 no caleAtac ' + xid + ' --> ' + fisier)
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
      print('err 154: căi atac ' + xid + ' ' + fisier + ' :: ' +str(e))
      breakpoint()
    
  return (sqlstart + 'VALUES ' + values)



def xmltodb(inputxmlz, xdbfile):
  conn = sqlite3.connect(xdbfile)
  cursor = conn.cursor()
  try:  
    zz = xmltodict.parse(gzip.GzipFile(inputxmlz))
  except:
    print('err 129 xmltodict.parse(gzip.GzipFile' + inputxmlz)
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
      instanta = 'xx-zz'
    

    try:
      linkpjr = str(int(float(instanta['link just-ro'])))
    except: 
      linkpjr = ''

    try:
      znr = instanta['tip']+'-'+linkpjr+'_'+dosar['numar']
      xnr = znr.iloc[0] #gets data from df
    except Exception as e:
      print('ERR 141: failed at xnr zrn ' + inputxmlz + ' --> '+ str(e))
      xnr = '?'
      znr = '?'
      return None

      if debugging:
        breakpoint()
 
    # TODO: add relational tables: parti, sedinte, caiatac
    # write dosar, DosarParte, DosarSedinta, DosarCaleAtac 
  
    sqlDosar = qiDosar(dosar, xnr)

    try:
      cursor.execute(sqlDosar)
    except sqlite3.Error as err:
        print('err 158 sqlDosar Query Failed: %s\nError: %s' % (sqlDosar, str(err)))
        if debugging:
          breakpoint()

    if 'parti' in dosar:
      sqlDosarParte = qiDosarParte(dosar, xnr)
      try:
        cursor.execute(sqlDosarParte)
      except sqlite3.Error as err:
          print('err 223 sqlDosarParte Query Failed: %s\nError: %s' % (sqlDosarParte, str(err)) + ' --> ' + inputxmlz)
          if debugging:
            breakpoint()
    
    if 'sedinte' in dosar:
      sqlDosarSedinta = qiDosarSedinta(dosar, xnr, inputxmlz)
      if sqlDosarSedinta:
        try:
          cursor.execute(sqlDosarSedinta)
        except sqlite3.Error as err:
            print('--err sqlDosarSedinta Query Failed: %s\nError: %s' % (sqlDosarSedinta, str(err)))
            if debugging:
              breakpoint()

    if 'caiAtac' in dosar:
      sqlCaleAtac = qiDosarCaiAtac(dosar, xnr, inputxmlz)
      if sqlCaleAtac:
        try:
          cursor.execute(sqlCaleAtac)
        except sqlite3.Error as err:
          print('err 242 sqlCaleAtac Query Failed: %s\nError: %s' % (sqlCaleAtac, str(err)) + ' --> ' + xnr)

  conn.commit()
  print('--> ' + inputxmlz) 


# loop all files in xmlgz, writhe to sqlite, move file

filez = [os.path.basename(x) for x in glob.glob(dir_xmlgz + "*.xml.gz")]
 
for file in filez:
  print('reading ' + dir_xmlgz + file)
  xmltodb(dir_xmlgz + file, dbfile)
  
  # move file
  os.rename(dir_xmlgz + file, dir_parsed + file)

  print('written to sql: ' + file)

print('>> DONE')