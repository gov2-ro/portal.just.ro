import spacy
from spacy import displacy

text = """
Admite propunerea de arestare preventivă formulată de D.I.I.C.O.T. – B.T. Mehedinţi, faţă de inculpaţii: MUNTEANU NICU-ALIN şi CROITORU DUMITRU-PETRI?OR, 
În baza art. 226 alin.2  Cpp,
Dispune arestarea preventivă pe o perioadă de 30 de zile, începând cu data de 28.10.2022 şi până la data de 26.11.2022, inclusiv, a inculpaţilor: 
- MUNTEANU NICU-ALIN, pentru săvârşirea infracţiunii de ,,trafic de droguri de risc”, în formă continuată,  prev. de art. 2 alin. 1 din Legea nr. 143/2000, privind prevenirea ?i combaterea traficului ?i consumului ilicit de droguri, cu aplicarea art. 35 alin. 1 Cod penal;
- CROITORU DUMITRU-PETRI?OR,  pentru săvârşirea infracţiunii de ,,trafic de droguri de risc”, în formă continuată,  prev. de art. 2 alin. 1 din Legea nr. 143/2000, privind prevenirea ?i combaterea traficului ?i consumului ilicit de droguri, cu aplicarea art. 35 alin. 1 Cod penal.-
În baza art. 230 Cpp, 
Dispune emiterea mandatelor de arestare preventivă pentru inculpaţii MUNTEANU NICU-ALIN şi CROITORU DUMITRU-PETRI?OR.
În baza art. 227 alin. 1 din C.p.p.,
Respinge propunerea de arestare preventivă formulată Ministerul Public - D.I.I.C.O.T. - B.T. Mehedinţi în dosarul nr. 10D/P/2022 faţă de inculpaţii :TIUTIUC DUMITRU, zis „Miky”, TUDOR GIGI-MARINEL, MARINCHESCU JIVORAD-?TEFAN zis ”Rocky”.
În baza art. 227 alin. 2 din C.p.p. rap. la art. 202 alin. 1, 2, 3 şi alin. 4 lit. b din C.p.p. coroborat cu art. 211 alin. 1 din C.p.p. şi art. 215 ind. 1 din C.p.p.,
Ia măsura preventivă a controlului judiciar pe o perioadă de 30 de zile începând cu data de 28.10.2022 şi până la data de 26.11.2022, inclusiv faţă de inculpaţii:
-TIUTIUC DUMITRU, zis „Miky”,  pentru săvârşirea infracţiunilor de „trafic de droguri de risc”, în formă continuată,  prev. de art. 2 alin. 1 din Legea nr. 143/2000, privind prevenirea ?i combaterea traficului ?i consumului ilicit de droguri, cu aplicarea art. 35 alin. 1 Cod penal;
- TUDOR GIGI-MARINEL, pentru săvârşirea infracţiunii de de ,,trafic de droguri de risc şi mare risc”, în formă continuată, prev. de art. 2 alin. 1 şi 2 din Legea nr. 143/2000 privind prevenirea ?i combaterea traficului ?i consumului ilicit de droguri, cu aplicarea art. 35 alin. 1 Cod penal;
-- MARINCHESCU JIVORAD-?TEFAN zis ”Rocky”,  pentru săvârşirea infracţiunilor de ,,trafic de droguri de risc”, în formă continuată,  prev. de art. 2 alin. 1 din Legea nr. 143/2000, privind prevenirea ?i combaterea traficului ?i consumului ilicit de droguri, cu aplicarea art. 35 alin. 1 Cod penal.
În temeiul art. 215 alin. 1 şi alin. 2 din C.p.p., 
Obligă pe inculpaţii TIUTIUC DUMITRU, zis „Miky”, TUDOR GIGI-MARINEL, MARINCHESCU JIVORAD-?TEFAN zis ”Rocky” :
    - să se prezinte la organul de urmărire penală, la judecătorul de drepturi şi libertăţi, la judecătorul de cameră preliminară sau la instanţa de judecată ori de câte ori este chemat;
    - să informeze de îndată organul judiciar care a dispus măsura sau în faţa căruia se află cauza cu privire la schimbarea locuinţei;
    - să se prezinte la I.P.J. Mehedinţi conform programului de supraveghere întocmit de organul de poliţie sau ori de câte ori este chemat;
     - să nu depăşească limita teritorială a judeţului Mehedinţi;
     - să nu se apropie şi să nu comunice direct sau indirect, pe nici o cale, cu martorii  PESCARU IONUŢ, DUMITRU GRIG AURELIAN, PRUNĂ MARIO LIVIU, BĂLĂCEANU DORU, BACIU GEORGE MARIAN, ŞAPTEBANI IULIAN, BRÎNZAN MIHAI, BILAVU RAIMONDO – MIHAIL – GEORGE, BUICĂ ALEXANDRU ARON, BECHERU MIHAI VALENTIN, MANGU LOREDANA – GEORGIANA, GIOTINĂ DANIEL CONSTANTIN, STANCA EMANUEL LUCIAN, GHEORGHE MARIUS, FUSU ALEX DIMITRIE, CĂRBUNARU MARIUS CRISTIAN,  cu colaboratorul sub acoperire DOBRE RAMONA, cu suspectul  ALMANI ALEXANDRU – DANIEL, precum şi cu inculpaţii din prezenta cauză.
     - să nu deţină, să nu folosească şi să nu poarte arme.
În temeiul art. 227 alin.1 teza finală, şi dispune punerea în libertate a inculpaţilor reţinuţi: TUDOR GIGI-MARINEL, MARINCHESCU JIVORAD-?TEFAN zis ”Rocky,” măsură ce va fi executorie de la expirarea ordonanţelor de reţinere dispuse faţă de aceşti inculpaţi.
În temeiul art. 215 alin. 3 din C.p.p.,
Atrage atenţia inculpaţilor că, în caz de încălcare cu rea-credinţă a măsurii sau a obligaţiilor care îi revin, măsura controlului judiciar poate fi înlocuită cu măsura arestului la domiciliu sau cu măsura arestării preventive. 
În temeiul art. 215 alin. 4 din C.p.p.,
Supravegherea respectării de către inculpat a obligaţiilor care îi revin pe durata controlului judiciar se va realiza de către I.P.J. Mehedinţi.
Copia minutei şi a încheierii se comunică. 
În baza art. 275 alin. 3 din C.p.p.,
Cheltuielile judiciare rămân în sarcina statului.
În baza art.275 alin.3 Cpp, cheltuielile judiciare avansate de stat rămân în sarcina acestuia, inclusiv sumele  de câte 680 lei, reprezentând onorariul avocaţilor din oficiu – Dumitraşcu Nicoleta şi Roşoga Cristian, potrivit delegaţiilor nr. 2861/28.10.2022 şi nr. 2860/28.10.2022, emise de Baroul Mehedinţi, sume ce vor  fi avansate  din fondurile Ministerului Justiţiei. 
Cu drept de contestaţie în 48 ore de la pronunţare.
Pronunţată în şedinţa din Camera de Consiliu,  azi 26.10.2022, orele 21.55, la sediul Tribunalului Mehedinţi.
"""

nlp = spacy.load("ro_core_news_lg")
doc = nlp(text)
displacy.serve(doc, style="ent")