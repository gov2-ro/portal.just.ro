import sqlite3, os

dbfile = "data/portal-just.db"

# clean-up first
# remove previous
os.remove(dbfile)

conn = sqlite3.connect(dbfile)
c = conn.cursor()
""" 
Dosar
DosarParte
DosarSedinta
DosarCaleAtac
Sedinta
SedintaDosar
 """

c.execute(
    """
          CREATE TABLE "Dosar" (
            "xnr"	TEXT NOT NULL UNIQUE,
            "numar"	TEXT NOT NULL,
            "Numar vechi"	TEXT,
            "data"	TEXT,
            "institutie"	TEXT,
            "categorieCaz"	TEXT,
            "stadiuProcesual"	TEXT,
            "parti"	TEXT,
            "sedinte"	TEXT,
            "caiAtac"	TEXT
          )
          """
)
c.execute(
    """
          CREATE TABLE "DosarParte" (
            "xnumardosar"  TEXT NOT NULL,
            "nume"	TEXT,
            "calitateParte"	TEXT
          )
          """
)
c.execute(
    """
          CREATE TABLE "DosarSedinta" (
            "xnumardosar"  TEXT NOT NULL,
            "complet" TEXT,
            "data" TEXT,
            "ora" TEXT,
            "soluţie" TEXT,
            "soluţieSumar" TEXT,
            "dataPronuntare" TEXT,
            "documentSedinta" TEXT,
            "numarDocument" TEXT,
            "dataDocument" TEXT
          )
          """
)

c.execute(
    """
          CREATE TABLE "DosarCaleAtac" (
            "xnumardosar"  TEXT NOT NULL,
            "dataDeclarare"	TEXT,
            "parteDeclaratoare"	TEXT,
            "tipCaleAtac"	TEXT
          )
          """
)

c.execute(
    """
          CREATE TABLE "Sedinta" (
            "xnrsedinta"  ID PRIMARY KEY,
            "departament"	TEXT,
            "complet"	TEXT,
            "data"	TEXT,
            "ora"	TEXT,
            "dosare"	TEXT
          )
          """
)
c.execute(
    """
          CREATE TABLE "SedintaDosar" (
            "xnrsedinta"  INT NOT NULL,
            "numar" TEXT NOT NULL UNIQUE,
            "numar vechi" TEXT,
            "data" TEXT,
            "ora" TEXT,
            "categorieCaz" TEXT,
            "stadiuProcesual" TEXT
          )
          """
)

conn.commit()

print('created ' + dbfile)