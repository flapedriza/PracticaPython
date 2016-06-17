import re
import os
import csv
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
    parameters = ["nom"] + ["latitud"] + ["longitud"] + ["tel1"] +
     ["tel2"] + ["adreca"] + ["barri"] + ["districte"] + ["cp"] +
     ["ciutat"] + ["regio"] + ["pais"] + ["web"] +
     ["propietari"] + ["mail"]

     for fila in csvreader:
        r = restaurant()
        for i in range(0,len(parameters)):
            r.__setattr__(parameters[i], fila[i])
        restaurants[r.nom] = r