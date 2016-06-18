#!/usr/bin/python
# coding=utf8

import csv
import re

from HTMLParser import HTMLParser

allrest=[]
EMAIL_FORMAT = re.compile(r'[^@]+@[^@]+\.[^@]+')
TELF_FORMAT = re.compile(r'\+[0-9]+\s.*')

class restaurant(object):
    nom = ""
    horari = ""
    latitud = ""
    longitud = ""
    telf1 = ""
    telf2 = ""
    adreca = ""
    barri = ""
    districte = ""
    cp = ""
    ciutat = ""
    regio = ""
    pais = ""
    web = ""    
    propietari = ""
    mail = ""

        
# creem una subclasse i sobreescribim el metodes del han
class MHTMLParser(HTMLParser):

    crest = restaurant()
    ctag = ""

    def handle_starttag(self, tag, attrs):
        self.ctag = tag
        if tag == 'v:vcard':
            self.crest = restaurant()
        elif (tag == 'v:url' and len(attrs) > 0):
            self.crest.web = attrs[0][1]
        elif (tag == 'rdf:description' and len(attrs) > 0):
            correu = attrs[0][1][7:]
            if(EMAIL_FORMAT.match(correu)): self.crest.mail = correu


    def handle_endtag(self, tag):
        self.ctag = ""
        if tag == 'v:vcard':
            allrest.append(self.crest)

    def handle_data(self, data):
        if self.ctag == 'v:fn':
            self.crest.nom = data
        elif(self.ctag == 'v:latitude'):
            self.crest.latitud = data
        elif(self.ctag == 'v:longitude'):
            self.crest.longitud = data
        elif(self.ctag == 'rdf:value'):
            if(TELF_FORMAT.match(data)):
                if(self.crest.telf1 == ""): self.crest.telf1 = data
                else: self.crest.telf2 = data
            else:
                self.crest.propietari = data
        elif(self.ctag == 'v:street-address'):
            self.crest.adreca = data
        elif(self.ctag == 'xv:neighborhood'):
            self.crest.barri = data
        elif(self.ctag == 'xv:district'):
            self.crest.districte = data
        elif(self.ctag == 'v:postal-code'):
            self.crest.cp = data
        elif(self.ctag == 'v:locality'):
            self.crest.ciutat = data
        elif(self.ctag == 'v:region'):
            self.crest.regio = data
        elif(self.ctag == 'v:country-name'):
            self.crest.pais = data
        
def genera_csv():
    try:
        f = open('restaurants.rdf', 'rb')
    except:
        print "No s'ha trobat l'arxiu restaurants.rdf"
        exit()
    rdfSource = f.read()
    f.close()

    parser = MHTMLParser()
    parser.feed(rdfSource)

    csvf = open('restaurants.csv', 'wb')
    fitxer = csv.writer(csvf, delimiter='\t')
    fitxer.writerow(["Nom"] + ["Latitud"] + ["Longitud"] + ["Telèfon 1"] + ["Telèfon 2"] +
    ["Adreça"] + ["Barri"] + ["Districte"] + ["Codi Postal"] + ["Ciutat"] + ["Regio"] +
    ["Pais"] + ["Web"] + ["Propietari"] + ["Correu electrònic"] )

    for elem in allrest:
        fitxer.writerow([elem.nom] + [elem.latitud] + [elem.longitud] + [elem.telf1] +
        [elem.telf2] + [elem.adreca] + [elem.barri] + [elem.districte] + [elem.cp] +
        [elem.ciutat] + [elem.regio] + [elem.pais] + [elem.web] +
        [elem.propietari] + [elem.mail])

    csvf.close()

