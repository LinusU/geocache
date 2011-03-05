#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from GeoCaching import GeoCaching

from optparse import OptionParser
from os.path import isdir

p = OptionParser(version=0.2)

p.add_option("-p", "--parse", dest="parse", help="Parse GCXXXX's from standard input", action="store_true", default=False)
p.add_option("-d", "--device", dest="device", help="Use the device DEV and set directories accordingly", metavar="DEV", default=None)
p.add_option("-o", "--output", dest="output", help="Fetch the caches to DIR", metavar="DIR", default="./")
p.add_option("-i", "--html", dest="html", help="Fetch the caches info as html to DIR", metavar="DIR", default=None)
p.add_option("-4", "--db4o", dest="db4o", help="Fetch the caches to a databse with the name DB", metavar="DB", default=None)

options, args = p.parse_args()

if options.parse:
    from re import findall
    from sys import stdin
    args += findall("(GC[0-9A-Z]+)\\b", stdin.read())

if options.device is not None:
    if options.db4o is None:
        options.output = "/media/%s/gpx/" % (options.device, )
    else:
        options.output = "/media/%s/gpx/database/" % (options.device, )
    options.html = "/media/%s/gpx/html/" % (options.device, )
    if not isdir(options.html): options.html = None

if options.output[-1] != "/":
    options.output += "/"

if not isdir(options.output):
    print "Output directory doesn't exists"
    quit(1)

if options.html is not None:
    
    if options.html[-1] != "/":
        options.html += "/"

    if not isdir(options.html):
        print "HTML directory doesn't exists"
        quit(2)
    

if options.db4o is not None:
    from GeoCaching import DB4O
    db = DB4O()
else:
    db = None

g = GeoCaching()

while len(args) > 0:
    gc = args.pop(0)
    
    if gc[:2] != "GC":
        continue
    
    if options.html is not None:
        g.fetch_html(options.html, gc)
    
    if db is None:
        f = open("%s%s.loc" % (options.output, gc), "w")
    else:
        f = db.create_loc(gc)
    
    try: g.fetch_loc(f, gc)
    except: args.append(gc)
    

if db is not None:
    db.save("%s%s.db4o" % (options.output, options.db4o))
    db = None
