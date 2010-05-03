#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from Login import Login

from urllib import urlencode
from urllib2 import urlopen

from optparse import OptionParser
from os.path import isdir

p = OptionParser(version=0.2)

p.add_option("-o", "--output", dest="output", help="Fetch the caches to DIR", metavar="DIR", default="./")

options, args = p.parse_args()

if options.output[-1] != "/":
    optins.output += "/"

if not isdir(options.output):
    print "Output directory doesn't exists"
    quit()

l = Login()

for gc in args:
    
    if gc[:2] != "GC":
        continue
    
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
    
