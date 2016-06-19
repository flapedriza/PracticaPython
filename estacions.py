#!/usr/bin/python
# coding=utf8

import urllib2
import xml.etree.ElementTree as XML
from math import radians, sin, cos, sqrt, asin

URL_BICING = "http://wservice.viabicing.cat/getstations.php?v=1"
RADI_TERRA = 6367.4447 #Km
STATION_ATTR = {
    'id':int,
    'street': str,
    'lat': float,
    'long': float,
    'height': float,
    'streetNumber': str,
    'status': str,
    'slots': int,
    'bikes': int
}

def haversine(lat1, lon1, lat2, lon2):
    """
    Càlcul de la distancia entre 2 punts geogràfics usant la fòrmula de Haversine
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = c * RADI_TERRA
    return km



class Estacio(object):
    def __str__(self):
        return "%s - %s%s (%s llocs | %s bicis)" % \
        (self.id, self.street, self.streetNumber, self.slots, self.bikes)
    def disponible(self):
        return self.status == 'OPN'
    def te_llocs(self):
        return self.slots > 0
    def te_bicis(self):
        return self.bikes > 0
    def distancia(self,latitud, longitud):
        return haversine(latitud, longitud, self.lat, self.long)

def getEstacions():
    ret = []
    request = urllib2.Request(URL_BICING)
    url = urllib2.urlopen(request)
    xml = url.read()
    url.close()
    reader = XML.fromstring(xml)
    for elem in reader.findall("station"):
        e = Estacio()
        for k, v in STATION_ATTR.items():
            text = elem.find(k).text
            if(k == 'streetNumber'):
                if(not text): text = ""
                else: text = ", " + text
            e.__setattr__(k, v(text))
        ret.append(e)
    return ret

def estacionsBicis(estacions):
    ret = [x for x in estacions if x.te_bicis() and x.disponible()]
    return ret

def estacionsLlocs(estacions):
    ret = [x for x in estacions if x.te_llocs() and x.disponible()]
    return ret

def estacions_a_prop(estacions, lat, lon):
    ret = []
    for e in estacions:
        dist = e.distancia(lat, lon)
        if dist <= 1:
            insert((dist,e), ret)

    return [y for (x,y) in ret]

def insert(elem, lst):
    if(len(lst) == 0): lst.append(elem)
    else:
        i = 0
        while lst[i][0] < elem[0] and i < len(lst)-1: i+=1
        lst.insert(i, elem)

if(__name__ == '__main__'):
    #41.385335, 2.169668 McDonald's Catalunya
    estac = getEstacions()
    print "\n\nAMB BICIS:"
    esta = estacionsBicis(estacions_a_prop(estac, 41.385335, 2.169668))
    for est in esta:
        print est
    esta = estacionsLlocs(estac)
    print "\n\nAMB LLOCS:"
    for est in esta:
        print est