#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from GeoCaching import GeoCaching

from pyquery import PyQuery
from optparse import OptionParser
from simplejson import dump, load
from os.path import isdir, isfile
from getpass import getpass
from sys import stdout

p = OptionParser(version=0.2)

p.add_option("-u", "--update", dest="update", help="If the JSON-file exists, update it", action="store_true", default=False)
p.add_option("-n", "--name", dest="name", help="Name the JSON-file NAME", metavar="NAME", default=None)
p.add_option("-d", "--device", dest="device", help="Use the device DEV and set directories accordingly", metavar="DEV", default=None)
p.add_option("-o", "--output", dest="output", help="Store the json in FILE", metavar="FILE", default=None)
p.add_option("-i", "--html", dest="html", help="Fetch the caches info as html to DIR", metavar="DIR", default=None)

options, args = p.parse_args()

if options.device is not None:
    options.output = "/media/%s/GeoLinus/%s.json" % (options.device, options.name)
    options.html = "/media/%s/GeoLinus/html/" % (options.device, )
    if not isdir(options.html): options.html = None

if options.output[-5:] != ".json":
    options.output += ".json"

if options.html is not None:
    
    if options.html[-1] != "/":
        options.html += "/"

    if not isdir(options.html):
        print "HTML directory doesn't exists"
        quit(2)

if len(args) != 4:
    print "Exactly 4 arguments is needed: lat1, lat2, lon1, lon2"
    quit(3)

u = raw_input("Username: ").strip()
p = getpass("Password: ").strip()

g = GeoCaching(u, p)

out = (load(open(options.output, "r")) if isfile(options.output) else list())
caches = g.fetch_window(float(args[0]), float(args[1]), float(args[2]), float(args[3]))

for i, obj in enumerate(caches):
    
    print "\r", "[" + str(i+1) + "/" + str(len(caches)) + "]",
    stdout.flush()
    
    try:
        if not obj['found']:
            del obj['found']
        if len(obj['hint'].trim()) == 0:
            del obj['hint']
    except: pass
    
    out = filter(lambda x: (x['gc'] != obj['gc']), out)
    out.append(obj)
    
    try:
        if options.html is not None and (not isfile(options.html + obj["gc"] + ".html") or options.update):
            g.fetch_html(options.html, obj["gc"])
    except:
        print "\nError fetching html for:", obj["gc"]
    

dump(out, open(options.output, "w"))
print 
