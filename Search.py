#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from Login import Login
from GeoForm import GeoForm
from GeoResult import GeoResult
from SearchCache import SearchCache

from gtk import main, main_quit
from gtk import Window, VBox

class Search(VBox):
    
    def __init__(self):
        
        VBox.__init__(self)
        
        self.form = GeoForm()
        self.result = GeoResult()
        
        self.pack_start(self.form, False)
        self.pack_start(self.result)
        
        self.login = Login()
        self.search = SearchCache(self.login)
        
        self.form.connect('search', self.do_search)
        
    
    def do_search(self, widget, lat, long):
        
        res = self.search.search_lat_long(lat, long)
        
        for row in res:
            self.result.add_cache(row)
        
        self.result.show_all()
        
    

if __name__ == '__main__':
    W = Window()
    S = Search()
    W.connect('destroy', main_quit)
    W.set_title("Search for caches")
    W.set_size_request(300,200)
    W.add(S)
    W.show_all()
    main()
