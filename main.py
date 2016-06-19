#!/usr/bin/python
# coding=utf8
import webbrowser
from sets import Set
from rdf2csv import restaurant, genera_csv
from searchRestaurants import guardaRestaurants, processaQuery
from estacions import Estacio, getEstacions, estacionsBicis, estacionsLlocs, estacions_a_prop

REST_ATTR = ["nom", "latitud", "longitud", "tel1",
   "tel2", "adreca", "barri", "districte", "cp",
   "ciutat", "regio", "pais", "web",
   "propietari", "mail"]

principi = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Resultats cerca</title>
</head>
<body>\n"""

segueix = """<table border="1" style="width:100%">
<tr style="background-color:#00FF00">
<td><b>Nom</b></td>
<td><b>Latitud</b></td>
<td><b>Longitud</b></td>
<td><b>Tel 1</b></td>
<td><b>Tel 2</b></td>
<td><b>Adreça</b></td>
<td><b>Barri</b></td>
<td><b>Districte</b></td>
<td><b>CP</b></td>
<td><b>Ciutat</b></td>
<td><b>Regió</b></td>
<td><b>País</b></td>
<td><b>Web</b></td>
<td><b>Propietari</b></td>
<td><b>Correu-e</b></td>
<td><b>Estacions amb Bicis Properes</b></td>
<td><b>Estacions amb Llocs Properes</b></td>
</tr>"""

final = """</table>
</body>
</html>"""

def posaEstacions(rest, estacions):
    aprop = estacions_a_prop(estacions, float(rest.latitud), float(rest.longitud))
    bicis = estacionsBicis(aprop)
    llocs = estacionsLlocs(aprop)
    strBici = "<ul>\n"
    strLloc = ""
    for est in bicis:
        strBici += "<li>%s</li>\n" % est
    for est in llocs:
        strLloc += "<li>%s</li>\n" % est
    strBici += "</ul>\n"
    strLloc += "</ul>\n"
    return (strBici, strLloc)

def creaTaula(restaurants, estacions):
    taula = ""
    for rest in restaurants:
        tuplaEst = posaEstacions(rest, estacions)
        taula += "<tr>\n"
        for attr in REST_ATTR:
            taula += "<td>" + getattr(rest, attr) + "</td>\n"
        taula += "<td>%s</td>\n<td>%s</td>\n</tr>\n" % tuplaEst
    return taula

def generaHtml(restaurants, estacions, cerca):
    f = open("restaurants.html", "w")
    f.write(principi)
    f.write("<p><b>Heu cercat: </b>%s i s'han retornat %s resultats</p>\n" % (cerca, len(restaurants)))
    f.write(segueix)
    f.write(creaTaula(restaurants, estacions))
    f.write(final)
    f.close()

if(__name__ == '__main__'):
    diccionariRest = guardaRestaurants()
    estacions = getEstacions()
    query = raw_input("Introduïu la cerca a realitzar:\n")
    rests = processaQuery(eval(query), Set(diccionariRest.keys()))
    rests = [diccionariRest[x] for x in rests]
    generaHtml(rests, estacions, query)
    webbrowser.open('restaurants.html')


