#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from cookielib import CookieJar
from urllib import urlencode
from urllib2 import Request, urlopen

class Login:
    
    def __init__(self):
        
        self.jar = CookieJar()
        self.req = Request("http://www.geocaching.com/login/default.aspx?RESET=Y", urlencode({
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            'ctl00$ContentBody$myUsername': 'SpaceStationOwner',
            'ctl00$ContentBody$myPassword': '921202lu',
            'ctl00$ContentBody$cookie': '',
            'ctl00$ContentBody$Button1': 'Login'
        }))
        
        self.jar.add_cookie_header(self.req)
        
        u = urlopen(self.req)
        
        self.jar.extract_cookies(u, self.req)
        
        u.close()
        
    
    def Request(self, *args):
        
        req = Request(*args)
        
        self.jar.add_cookie_header(req)
        
        return req
        
    
    def urlopen(self, *args):
        
        r = self.Request(*args)
        
        return urlopen(r)
        
    
