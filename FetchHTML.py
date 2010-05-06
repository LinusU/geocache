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

def get_guid(login, gc):
    
    u = login.urlopen("http://www.geocaching.com/seek/cache_details.aspx?wp=%s" % (gc, ))
    
    s1 = u.read(1024)
    s2 = u.read(1024)
    
    while len(s1) + len(s2) != 0:
        
        re = GUID.search(s1 + s2)
        
        if re:
            return re.group(1)
        
        s1 = s2
        s2 = u.read(1024)
        
    
    return False
    

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
    

def FetchHTML(login, gc, output):
    
    guid = get_guid(login, gc)
    
    if guid is False:
        return False
    
    u = login.urlopen("http://www.geocaching.com/seek/cdpf.aspx?guid=%s&lc=10" % (guid, ))
    f = open("%s%s.html" % (output, gc), 'w')
    
    line = u.readline()
    
    if line[0] in ("\r", "\n"):
        line = '<?xml version="1.0" encoding="utf-8" ?>' + line
    elif line[0:9] == "<!DOCTYPE":
        line = '<?xml version="1.0" encoding="utf-8" ?>' + "\n" + line
    
    f.write(line)
    
    for line in u:
        
        line = SCRIPTS.sub('', line)
        line = IMAGES.sub(lambda m: image(m, login, gc, output), line)
        line = LINKS.sub(lambda m: link(m, login, gc, output), line)
        
        f.write(line)
        
    
    u.close()
    f.close()
    
    return True
    
