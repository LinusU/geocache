#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from re import compile
from base64 import b64encode
from os import mkdir
from os.path import isdir, exists

GUID = compile('href="cdpf.aspx\?guid=([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})(&lc=[0-9]+)?"')

SCRIPTS = compile('<script[^>]*></script>')
IMAGES = compile('<img[^>]*src="([^"]+)"[^>]*>')
LINKS = compile('<a[^>]*href="([^"]+)"[^>]*>')

def script(match, login, gc, output):
    
    return ''
    

def image(match, login, gc, output):
    
    if not isdir("%simg/" % (output, )):
        mkdir("%simg/" % (output, ))
    
    if match.group(1)[:7] == "http://":
        url = match.group(1)
    elif match.group(1)[:1] == "/":
        url = "http://www.geocaching.com%s" % (match.group(1), )
    else:
        url = "http://www.geocaching.com/seek/%s" % (match.group(1), )
    
    name = "img/%s.%s" % (b64encode(match.group(1)), match.group(1)[-3:])
    
    if not exists("%s%s" % (output, name)):
        
        u = login.urlopen(url)
        f = open("%s%s" % (output, name), 'w')
        
        s = u.read(1024)
        
        while len(s) > 0:
            f.write(s)
            s = u.read(1024)
        
        u.close()
        f.close()
        
    
    return match.group(0)[:match.start(1)-match.start(0)] + name + match.group(0)[match.end(1)-match.end(0):]
    

def link(match, login, gc, output):
    
    if match.group(1)[:11] == "javascript:":
        return match.group(0)
    
    if match.group(1)[:7] == "http://":
        url = match.group(1)
    elif match.group(1)[:1] == "/":
        url = "http://www.geocaching.com%s" % (match.group(1), )
    else:
        url = "http://www.geocaching.com/seek/%s" % (match.group(1), )
    
    return match.group(0)[:match.start(1)-match.start(0)] + url + match.group(0)[match.end(1)-match.end(0):]
    
