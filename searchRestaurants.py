#!/usr/bin/python
# coding=utf8

import re
import os
import csv
from sets import Set
from rdf2csv import restaurant, genera_csv

restaurants = {}
STRING_FORM = re.compile(r'[\"\']?\w+[\s\w*]*[\"\']?')


def guardaRestaurants():
    ret = {}
    try:
        restcsv = open('restaurants.csv', 'rb')
    except:
        print "restaurants.csv no trobat, generant..."
        genera_csv()
        restcsv = open('restaurants.csv','rb')
    csvreader = csv.reader(restcsv, delimiter='\t')
    parameters = (["nom"] + ["latitud"] + ["longitud"] + ["tel1"] +
    ["tel2"] + ["adreca"] + ["barri"] + ["districte"] + ["cp"] +
    ["ciutat"] + ["regio"] + ["pais"] + ["web"] +
    ["propietari"] + ["mail"])
    for fila in csvreader:
        r = restaurant()
        for i in range(0,len(parameters)):
            r.__setattr__(parameters[i], fila[i])
        ret[r.nom] = r
    return ret

def processaQuery(query, llista):
    try:
        if(STRING_FORM.match(query) is None):
            query = eval(query)
    except:
        pass
    if(isinstance(query, list)):
        #Complir una condició -> unió
        ret = Set()
        for elem in query:
            ret = ret.union(processaQuery(elem, llista.difference(ret)))
        return ret
    elif(isinstance(query, tuple)):
        #complir totes les condicions -> buscar al resultat anterior
        ret = llista
        for elem in query:
            ret = processaQuery(elem, ret)
        return ret
    elif(isinstance(query, str)):
        #Buscar el string a la llista de noms
        ret = [x for x in llista if query in x]
        return Set(ret)

if __name__ == "__main__":
    restaurants = guardaRestaurants()
    query = raw_input("Introduïu els criteris de cerca:\n")
    rests = processaQuery(eval(query), Set(restaurants.keys()))
    print len(rests)
