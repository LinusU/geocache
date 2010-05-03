#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from gtk import Table, Label, image_new_from_file
from gtk import EXPAND, FILL, JUSTIFY_LEFT
from pango import ELLIPSIZE_END

class GtkCache(Table):
    
    def __init__(self, info):
        
        Table.__init__(self, 4, 1)
        
        self.info = info
        
        self.objs = (
            image_new_from_file("img/found/%s.png" % (str(self.info['found']), )),
            image_new_from_file("img/wpt/%s.png" % (self.info['type'][0], )),
            Label(self.info['id']),
            Label("%s by %s" % (self.info['name'], self.info['creator']))
        )
        
        self.objs[0].set_tooltip_text("Found" if self.info['found'] else "Not found")
        self.objs[1].set_tooltip_text(self.info['type'][1])
        
        self.objs[2].set_size_request(80, 32)
        self.objs[3].set_justify(JUSTIFY_LEFT)
        self.objs[3].set_ellipsize(ELLIPSIZE_END)
        
        self.attach(self.objs[0], 0, 1, 0, 1, FILL, FILL)
        self.attach(self.objs[1], 1, 2, 0, 1, FILL, FILL)
        self.attach(self.objs[2], 2, 3, 0, 1, FILL, FILL, FILL, FILL)
        self.attach(self.objs[3], 3, 4, 0, 1)
        
    
