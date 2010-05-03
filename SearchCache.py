#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from re import compile
from HTMLParser import HTMLParser, HTMLParseError

WptType = compile("/images/WptTypes/([0-9])\.gif")
DifficultyTerrain = compile("\(([1-5]\.?5?)/([1-5]\.?5?)\)")
Date = compile("([0-9]{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([0-9]{2})")
By = compile("by (.*) \((GC[0-9A-Z]{4})\)")

def month2dec(month):
    if month == "Jan": return 1
    elif month == "Feb": return 2
    elif month == "Mar": return 3
    elif month == "Apr": return 4
    elif month == "May": return 5
    elif month == "Jun": return 6
    elif month == "Jul": return 7
    elif month == "Aug": return 8
    elif month == "Sep": return 9
    elif month == "Oct": return 10
    elif month == "Nov": return 11
    elif month == "Dec": return 12

class SearchCache(HTMLParser):
    
    def __init__(self, login):
        
        HTMLParser.__init__(self)
        
        self.login = login
        self.list = 0
        
        self.results = list()
        self.item = None
        self.fill = None
        self.next = None
        
    
    def new_item(self):
        
        self.item = {
            'id': '',
            'found': False,
            'type': (0, "Unknown"),
            'name': '',
            'creator': '',
            'difficulty': '',
            'terrain': '',
            'country': '',
            'state': '',
            'date': (1970, 1, 1)
        }
        
    
    def search_lat_long(self, lat, long):
        
        u = self.login.urlopen(
            "http://www.geocaching.com/seek/nearest.aspx?lat=%f&lng=%f" % (lat, long)
        )
        
        s = u.read(1024)
        
        while len(s) > 0:
            try: self.feed(s)
            except HTMLParseError: pass
            s = u.read(1024)
        
        u.close()
        
        try: self.close()
        except HTMLParseError: pass
        
        return self.results
        
    
    def close(self):
        
        if self.item is not None:
            self.results.append(self.item)
        
        self.item = None
        
        HTMLParser.close(self)
        
    
    def handle_starttag(self, tag, attrs):
        
        attrs = dict(attrs)
        
        if attrs.has_key('class'):
            classes = attrs['class'].split(" ")
        else:
            classes = list()
        
        if tag == 'table' and ("SearchResultsTable" in classes or self.list):
            self.list += 1
        
        if self.list == 0:
            return
        
        if tag == 'tr' and "Data" in classes:
            
            if self.item is not None:
                self.results.append(self.item)
            
            self.new_item()
            
        
        if self.item is None:
            return
        
        if tag == 'img' and (attrs['src'] == "/images/WptTypes/check.gif" or attrs['alt'] == "Found It!"):
            self.item['found'] = True
        
        if tag == 'a' and attrs['href'] == "/about/cache_types.aspx":
            self.next = 'type'
        
        if tag == 'img' and self.next == 'type':
            re = WptType.match(attrs['src'])
            if re:
                self.item['type'] = (re.group(1), attrs['alt'])
            else:
                self.item['type'] = (0, attrs['alt'])
            self.next = None
        
        if tag == 'a' and attrs['href'][:24] == "/seek/cache_details.aspx":
            self.fill = 'name'
        
    
    def handle_endtag(self, tag):
        
        if(
            self.item is not None and
            self.fill is not None and
            len(self.item[self.fill]) > 0
        ):
            self.fill = None
        
        if tag == 'table' and self.list:
            self.list -= 1
        
    
    def handle_data(self, data):
        
        if self.item is None:
            return
        
        #FIXME: do the below with Regex
        
        data = data.strip()
        data = data.replace("\r", "")
        data = data.replace("\n", " ")
        data = data.replace("  ", " ")
        
        if self.fill is not None and self.item is not None:
            self.item[self.fill] += data
        
        re = DifficultyTerrain.search(data)
        
        if re:
            self.item['difficulty'] = re.group(1)
            self.item['terrain'] = re.group(2)
        
        if not self.item.has_key('date'):
            
            re = Date.search(data)
            
            if re:
                self.item['date'] = (re.group(3), month2dec(re.group(2)), re.group(1))
            
        
        re = By.search(data)
        
        if re:
            self.item['creator'] = re.group(1)
            self.item['id'] = re.group(2)
            self.fill = "state"
        
    
    def handle_charref(self, name):
        
        if self.fill is not None and self.item is not None:
            self.item[self.fill] += unichr(int(name))
        
    
