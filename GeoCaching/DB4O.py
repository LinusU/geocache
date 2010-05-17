#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# © Linus Unnebäck
#

from os import remove, rmdir
from shutil import move
from os.path import join
from tempfile import mkdtemp
from subprocess import call

class DB4O:
    
    def __init__(self):
        
        self.dir = mkdtemp()
        self.files = []
        
    
    def __del__(self):
        rmdir(self.dir)
    
    def create_loc(self, gc):
        
        fn = join(self.dir, "%s.loc" % (gc, ))
        
        self.files.append(fn)
        
        return open(fn, 'w')
        
    
    def save(self, filename):
        
        call(["java", "-jar", "odbmgmt.jar", "-d"])
        call(["java", "-jar", "odbmgmt.jar", "-a", self.dir])
        
        move("database.db4o", filename)
        
        for f in self.files:
            remove(f)
        
    
