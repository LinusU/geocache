#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from re import compile
from HTMLParser import HTMLParser, HTMLParseError
from htmlentitydefs import name2codepoint
from datetime import date

WptType = compile("/images/WptTypes/([0-9])\.gif")
DifficultyTerrain = compile("\(([1-5]\.?5?)/([1-5]\.?5?)\)")
Date = compile("([0-9]{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) ([0-9]{2})")
By = compile("by (.*) \((GC[0-9A-Z]{4,6})\)")

def month2int(month):
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

class SearchParser(HTMLParser):
    
    def __init__(self, login):
        
        HTMLParser.__init__(self)
        
        self.login = login
        self.list = 0
        
        self.results = list()
        self.item = None
        self.fill = None
        self.next = None
        
        self.data = unicode("")
        
    
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
            'date': date(1970, 1, 1)
        }
        
    
    def parse_stream(self, stream):
        
        s = stream.read(1024)
        
        while len(s) > 0:
            try: self.feed(s)
            except HTMLParseError: pass
            s = stream.read(1024)
        
        stream.close()
        
        try: self.close()
        except HTMLParseError: pass
        
        return True
        
    
    def close(self):
        
        if self.item is not None:
            self.results.append(self.item)
        
        self.item = None
        
        HTMLParser.close(self)
        
    
    def handle_starttag(self, tag, attrs):
        
        self.process_data()
        
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
        
        self.process_data()
        
        if(
            self.item is not None and
            self.fill is not None and
            len(self.item[self.fill]) > 0
        ):
            self.fill = None
        
        if tag == 'table' and self.list:
            self.list -= 1
        
    
    def handle_data(self, data):
        self.data += unicode(data)
    
    def handle_charref(self, name):
        self.data += unichr(int(name))
    
    def handle_entityref(self, name):
        
        if name in name2codepoint:
            self.data += unichr(name2codepoint[name])
        else:
            self.data += u"?"
        
    
    def process_data(self):
        
        if self.item is None:
            return
        
        self.data = self.data.strip()
        
        if len(self.data) == 0:
            return
        
        data = unicode("")
        space = False
        
        for c in self.data:
            if c == "\n":
                if not space:
                    data += u" "
                    space = True
            elif c == "\r":
                pass
            elif c == " ":
                if not space:
                    data += u" "
                    space = True
            else:
                data += c
                space = False
        
        self.data = unicode("")
        
        if self.fill is not None and self.item is not None:
            self.item[self.fill] = data
        
        re = DifficultyTerrain.search(data)
        
        if re:
            self.item['difficulty'] = re.group(1)
            self.item['terrain'] = re.group(2)
        
        if self.item['date'] is None:
            
            re = Date.search(data)
            
            if re:
                self.item['date'] = date(
                    int(re.group(3)),
                    month2int(re.group(2)),
                    int(re.group(1))
                )
            
        
        re = By.search(data)
        
        if re:
            self.item['creator'] = re.group(1)
            self.item['id'] = re.group(2)
            self.fill = "state"
        
    
