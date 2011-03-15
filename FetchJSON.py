#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from GeoCaching import GeoCaching

from pyquery import PyQuery
from optparse import OptionParser
from os.path import isdir, isfile
from re import findall
from simplejson import dump, load
from codecs import lookup
from getpass import getpass

p = OptionParser(version=0.2)

p.add_option("-a", "--append", dest="append", help="If the JSON-file exists, append to it", action="store_true", default=False)
p.add_option("-u", "--update", dest="update", help="If the JSON-file exists, update it", action="store_true", default=False)
p.add_option("-p", "--parse", dest="parse", help="Parse GCXXXX's from standard input", action="store_true", default=False)
p.add_option("-n", "--name", dest="name", help="Name the JSON-file NAME", metavar="NAME", default=None)
p.add_option("-d", "--device", dest="device", help="Use the device DEV and set directories accordingly", metavar="DEV", default=None)
p.add_option("-o", "--output", dest="output", help="Store the json in FILE", metavar="FILE", default=None)
p.add_option("-i", "--html", dest="html", help="Fetch the caches info as html to DIR", metavar="DIR", default=None)

options, args = p.parse_args()

u = raw_input("Username: ").strip()
p = getpass("Password: ").strip()

if options.parse:
    from sys import stdin
    args += findall("(GC[0-9A-Z]+)\\b", stdin.read())

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

g = GeoCaching(u, p)
gcs = list()
out = list()
rot13 = lookup('rot_13')

if options.append or options.update:
    for obj in load(open(options.output, "r")):
        try:
            if not options.update:
                gcs.append(obj['gc'])
            out.append(obj)
        except: pass

while len(args) > 0:
    gc = args.pop(0)
    
    if gc[:2] != "GC":
        continue
    
    if gc not in gcs:
        
        try:
            
            d = PyQuery(url="http://www.geocaching.com/seek/cache_details.aspx?wp=%s" % (gc, ), opener=lambda url: g.urlopen(url).read())
            obj = dict()
            
            obj['gc'] = gc
            
            try:
                obj['type'] = int(findall("[0-9]+", d('td.cacheImage img').attr("src")).pop())
                obj['title'] = d('[id="ctl00_ContentBody_CacheName"]').text()
                obj['found'] = (len(d('[id="ctl00_ContentBody_hlFoundItLog"]')) > 0)
                obj['hint'] = rot13.decode(d('[id="div_hint"]').text())[0]
            except: pass
            
            try:
                if not obj['found']:
                    del obj['found']
                if len(obj['hint'].trim()) == 0:
                    del obj['hint']
            except: pass
            
            geo = findall('([NS]) ([0-9]{2})° ([0-9]+\.[0-9]+) ([EW]) ([0-9]{3})° ([0-9]+\.[0-9]+)', d('[id="ctl00_ContentBody_LatLon"]').text()).pop()
            
            obj['lat'] = int(round((int(geo[1]) + (float(geo[2]) / 60)) * (1 if geo[0] == "N" else -1) * 1E6))
            obj['lon'] = int(round((int(geo[4]) + (float(geo[5]) / 60)) * (1 if geo[3] == "E" else -1) * 1E6))
            
            out = filter(lambda x: (x['gc'] != obj['gc']), out)
            
            gcs.append(gc)
            out.append(obj)
            
        except:
            
            print "Failed to fetch cache: ", gc
            
        
    
    if options.html is not None and (not isfile(options.html + gc + ".html") or options.update):
        try:
            from GeoCaching.HTML import GUID
            guid = GUID.findall(d('[id="ctl00_ContentBody_lnkPrintFriendly"]').attr('href')).pop()
            g.fetch_html(options.html, gc, guid)
        except:
            g.fetch_html(options.html, gc)
    

dump(out, open(options.output, "w"))

print "All done"
