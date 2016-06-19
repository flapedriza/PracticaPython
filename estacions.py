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
    def disponible():
        return self.status == 'OPN'
    def te_aparcaments():
        return self.slots > 0
    def te_bicis():
        return self.bikes > 0
    def distancia(latitud, longitud):
        return haversine(latitud, longitud, self.lat, self.long)

def getEstacions():
    ret = {}
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
        ret[e.id] = e
    return ret

esta = getEstacions()
for e in esta.values():
    print e