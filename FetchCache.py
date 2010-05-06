#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from Login import Login
from FetchHTML import FetchHTML

from urllib import urlencode
from urllib2 import urlopen

from optparse import OptionParser
from os.path import isdir

p = OptionParser(version=0.2)

p.add_option("-d", "--device", dest="device", help="Use the device DEV and set directories accordingly", metavar="DEV", default=None)
p.add_option("-o", "--output", dest="output", help="Fetch the caches to DIR", metavar="DIR", default="./")
p.add_option("-i", "--html", dest="html", help="Fetch the caches info as html to DIR", metavar="DIR", default=None)

options, args = p.parse_args()

if options.device is not None:
    options.output = "/media/%s/gpx/" % (options.device, )
    options.html = "/media/%s/gpx/html/" % (options.device, )

if options.output[-1] != "/":
    optins.output += "/"

if not isdir(options.output):
    print "Output directory doesn't exists"
    quit(1)

if options.html is not None:
    
    if options.html[-1] != "/":
        optins.html += "/"

    if not isdir(options.html):
        print "HTML directory doesn't exists"
        quit(2)
    

l = Login()

for gc in args:
    
    if gc[:2] != "GC":
        continue
    
    if options.html is not None:
        FetchHTML(l, gc, options.html)
    
    r = l.Request(
        "http://www.geocaching.com/seek/cache_details.aspx?wp=%s" % (gc,),
        urlencode({
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            'ctl00$ContentBody$btnLocDL': 'LOC Waypoint File'
        })
    )
    
    u = urlopen(r)
    f = open("%s%s.loc" % (options.output, gc), 'w')
    
    s = u.read(1024)
    
    while len(s) > 0:
        f.write(s)
        s = u.read(1024)
    
    u.close()
    f.close()
    
