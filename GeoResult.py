#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from GtkCache import GtkCache

from gtk import ScrolledWindow, VBox
from gtk import POLICY_NEVER, POLICY_ALWAYS

from urllib2 import urlopen
from xml.dom.minidom import parse

class GeoResult(ScrolledWindow):
    
    def __init__(self):
        
        ScrolledWindow.__init__(self)
        
        self.set_policy(POLICY_NEVER, POLICY_ALWAYS)
        
        self.box = VBox()
        
        self.add_with_viewport(self.box)
        
    
    def add_cache(self, cache):
        
        self.box.pack_start(GtkCache(cache))
        
    '''
    def search_lat_long(self, login, lat, long):
        
        r = login.Request("http://www.geocaching.com/seek/nearest.aspx?lat=%f&lng=%f" % (lat, long))
        u = urlopen(r)
        
        dom = parse(u)
        
        table = dom.documentElement.getElementById("ctl00_ContentBody_dlResults")
        
        rows = table.getElementsByTagName("tr")
        
        for row in rows:
            
            r = row.getElementsByTagName("td")[0]
            r = r.getElementsByTagName("tr")[0]
            
            if "data" in r.getAttribute("class").split(" "):
                
            
        
    '''
