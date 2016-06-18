#!/usr/bin/python
# coding=utf8

import re
import os
import csv
from sets import Set
from rdf2csv import restaurant

restaurants = {}

def guardaRestaurants():
    global restaurants
    try:
        restcsv = open('restaurants.csv', 'rb')
    except:
        execfile("rdf2csv.py")
        restcsv = open('restaurants.csv','rb')
    csvreader = csv.reader(restcsv)
    parameters = (["nom"] + ["latitud"] + ["longitud"] + ["tel1"] +
    ["tel2"] + ["adreca"] + ["barri"] + ["districte"] + ["cp"] +
    ["ciutat"] + ["regio"] + ["pais"] + ["web"] +
    ["propietari"] + ["mail"])
    for fila in csvreader:
        r = restaurant()
        for i in range(0,len(parameters)):
            r.__setattr__(parameters[i], fila[i])
        restaurants[r.nom] = r

#def trobaRestaurants(patro, llista):
#    return [x for x in llista if patro in x]

def processaQuery(query, llista):
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
        return [x for x in llista if patro in x]


def main():
    guardaRestaurants()
    input = raw_input("Quina cerca voleu fer?\n")
    rests = processaQuery(eval(query), Set(restaurants.keys()))
    print rests

