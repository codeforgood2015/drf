# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 17:28:04 2015
Ok, what's going on ENCODING?

@author: LLP-admin
"""
string = unicode('café', 'utf8')
string_out = string.encode('utf8', 'replace')
log = open('test.txt', 'w')
log.write(string_out)

