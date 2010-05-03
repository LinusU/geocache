#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from gtk import Table, Label, Entry, Button
from gobject import SIGNAL_ACTION, TYPE_NONE, TYPE_FLOAT

from re import compile

FMT1 = compile("-?[0-9]+\.[0-9]+")

FMT2 = compile("([0-9]+)° ([0-9]+.[0-9]+)[′']? (N|S)")
FMT3 = compile("([0-9]+)° ([0-9]+.[0-9]+)[′']? (E|W)")

FMT4 = compile("(N|S) ([0-9]+)° ([0-9]+.[0-9]+)[′']?")
FMT5 = compile("(E|W) ([0-9]+)° ([0-9]+.[0-9]+)[′']?")

def geo2dec(lat, long):
    
    r1, r2 = "", ""
    
    if lat[0] == "S": r1 += "-"
    if long[0] == "W": r2 += "-"
    
    r1 += str(float(lat[1]) + float(lat[2]) / 60)
    r2 += str(float(long[1]) + float(long[2]) / 60)
    
    return float(r1), float(r2)
    

class GeoForm(Table):
    
    __gsignals__ = {
        'search': (SIGNAL_ACTION, TYPE_NONE, (TYPE_FLOAT, TYPE_FLOAT))
    }
    
    def __init__(self):
        
        Table.__init__(self, 1, 5)
        
        self.entry1 = Entry()
        self.entry2 = Entry()
        
        self.button = Button("Search")
        
        self.attach(self.entry1, 0, 1, 0, 1) 
        self.attach(self.entry2, 1, 2, 0, 1) 
        self.attach(self.button, 2, 3, 0, 1)
        
        self.entry1.set_width_chars(12)
        self.entry2.set_width_chars(12)
        
        self.entry1.set_text("59.666042")
        self.entry2.set_text("16.481794")
        
        self.button.connect('clicked', self.clicked)
        
    
    def get_lat_long(self):
        
        s1 = self.entry1.get_text()
        s2 = self.entry2.get_text()
        
        re1 = FMT1.match(s1)
        re2 = FMT1.match(s2)
        
        if re1 and re2:
            return float(re1.group(0)), float(re2.group(0))
        
        re1 = FMT2.match(s1)
        re2 = FMT3.match(s2)
        
        if re1 and re2:
            c1 = re1.group(3), re1.group(1), re1.group(2)
            c2 = re2.group(3), re2.group(1), re2.group(2)
            return geo2dec(c1, c2)
        
        re1 = FMT4.match(s1)
        re2 = FMT5.match(s2)
        
        if re1 and re1:
            c1 = re1.group(1), re1.group(2), re1.group(3)
            c2 = re2.group(1), re2.group(2), re2.group(3)
            return geo2dec(c1, c2)
        
        raise SyntaxError()
        
    
    def clicked(self, event):
        
        try:
            self.emit('search', *self.get_lat_long())
        except SyntaxError: pass
            #FIXME: make background red
        
    
