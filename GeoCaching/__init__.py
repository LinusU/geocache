#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from DB4O import DB4O

from cookielib import CookieJar
from urllib import urlencode
from urllib2 import Request, urlopen
from simplejson import load, loads

class GeoCaching:
    
    def __init__(self, username='SpaceStationOwner', password='921202lu'):
        
        self.jar = CookieJar()
        self.req = Request("http://www.geocaching.com/login/default.aspx?RESET=Y", urlencode({
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            'ctl00$ContentBody$myUsername': username,
            'ctl00$ContentBody$myPassword': password,
            'ctl00$ContentBody$cookie': '',
            'ctl00$ContentBody$Button1': 'Login'
        }))
        
        self.jar.add_cookie_header(self.req)
        
        u = urlopen(self.req)
        
        self.jar.extract_cookies(u, self.req)
        
        u.close()
        
    
    def urlopen(self, *args):
        
        req = Request(*args)
        
        self.jar.add_cookie_header(req)
        
        return urlopen(req)
        
    
    def urlfetch(self, output, *args):
        
        u = self.urlopen(*args)
        
        if hasattr(output, "write"):
            f = output
        else:
            f = open(output, 'w')
        
        s = u.read(1024)
        
        while len(s) > 0:
            f.write(s)
            s = u.read(1024)
        
        u.close()
        f.close()
        
    
    def get_guid(self, gc):
        
        from HTML import GUID
        
        u = self.urlopen("http://www.geocaching.com/seek/cache_details.aspx?wp=%s" % (gc, ))
        
        s1 = u.read(1024)
        s2 = u.read(1024)
        
        while len(s1) + len(s2) != 0:
            
            re = GUID.search(s1 + s2)
            
            if re:
                u.close()
                return re.group(1)
            
            s1 = s2
            s2 = u.read(1024)
            
        
        u.close()
        
        return False
        

    def fetch_loc(self, fileobject, gc):
        
        self.urlfetch(
            fileobject,
            "http://www.geocaching.com/seek/cache_details.aspx?wp=%s" % (gc, ),
            urlencode({
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': '',
                'ctl00$ContentBody$btnLocDL': 'LOC Waypoint File'
            })
        )
        
        return True
        
    
    def fetch_html(self, directory, gc, guid = None):
        
        from HTML import SCRIPTS, IMAGES, LINKS
        from HTML import script, image, link
        
        if guid is None:
            guid = self.get_guid(gc)
        
        if guid is False:
            return False
        
        u = self.urlopen("http://www.geocaching.com/seek/cdpf.aspx?guid=%s&lc=10" % (guid, ))
        f = open("%s%s.html" % (directory, gc), 'w')
        
        line = u.readline()
        
        if line[0] in ("\r", "\n"):
            line = '<?xml version="1.0" encoding="utf-8" ?>' + line
        elif line[0:9] == "<!DOCTYPE":
            line = '<?xml version="1.0" encoding="utf-8" ?>' + "\n" + line
        
        f.write(line)
        
        for line in u:
            
            line = SCRIPTS.sub(lambda m: script(m, self, gc, directory), line)
            line = IMAGES.sub(lambda m: image(m, self, gc, directory), line)
            line = LINKS.sub(lambda m: link(m, self, gc, directory), line)
            
            f.write(line)
            
        
        u.close()
        f.close()
        
        return True
        
    
    def search_lat_long(self, lat, long):
        
        from SearchParser import SearchParser
        
        s = SearchParser(self)
        
        s.parse_stream(self.urlopen(
            "http://www.geocaching.com/seek/nearest.aspx?lat=%f&lng=%f" % (lat, long)
        ))
        
        return s
        
    
    def fetch_window(self, lat1, lat2, lon1, lon2):
        
        if lat2 > lat1: lat1, lat2 = lat2, lat1
        if lon2 > lon1: lon1, lon2 = lon2, lon1
        
        f = self.urlopen(
            "http://www.geocaching.com/map/default.aspx/MapAction",
            '{"dto":{"data":{"c":1,"m":"","d":"%.9f|%.9f|%.9f|%.9f"},"ut":""}}' % (lat1, lat2, lon1, lon2),
            {
                "Origin": "http://www.geocaching.com",
                "Content-Type": "application/json"
            }
        )
        
        j = load(f)
        j = loads(j["d"])
        
        ret = list()
        
        for obj in j["cs"]["cc"]:
            ret.append({
                "gc": obj["gc"],
                "type": obj["ctid"],
                "title": obj["nn"],
                "lat": int(round(obj["lat"] * 1E6)),
                "lon": int(round(obj["lon"] * 1E6)),
                "found": obj["f"],
                "disabled": not obj["ia"]
            })
        
        return ret
        
    
