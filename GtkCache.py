#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from gtk import Table, Label, image_new_from_file

class GtkCache(Table):
    
    def __init__(self, info):
        
        Table.__init__(self, 10, 2, True)
        
        self.info = info
        
        self.attach(Label(str(self.info['found'])), 0, 1, 0, 1)
        self.attach(image_new_from_file("img/wpt/%s.png" % (self.info['type'][0], )), 1, 2, 0, 1)
        self.attach(Label(self.info['type'][1]), 2, 3, 0, 1)
        self.attach(Label(self.info['name']), 3, 4, 0, 1)
        
    
