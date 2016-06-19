#!/usr/bin/python
# coding=utf8

import urllib2
import xml.etree.ElementTree as XML
import math

URL_BICING = "http://wservice.viabicing.cat/getstations.php?v=1"

class Estacio(object):
    id = None
    street = None
    streetNumber = None
    lat = None
    long = None
    height = None
    slots = None
    bikes = None
    status = None

    def __str__(self):
        return "%s - %s, %s" % (self.id, self.carrer, self.numCarrer)



