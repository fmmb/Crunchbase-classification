#!/usr/bin/python
# -*- coding: utf-8 -*-

def Help():
    print >> sys.stderr, '''
================================================================================
Reads a file with tagged examples, selects allowed tags and randomizes data
Fernando Manuel Marques Batista  -  (c) Copyright 2014 -  Ver: 1.0 (unstable)
--------------------------------------------------------------------------------
Usage: %s [-h] [-v] data.json[.gz] 

options:
    -h : shows this help
    -q : low verbosity
    -alltags : does not restrict tags to a predefined set of classes
'''%sys.argv[0]
    quit()

# Imports
# ------------------------------------------------------------------------------

import re
import sys
import gzip
import math
import operator
import collections
import random
import json

# Default values
# ------------------------------------------------------------------------------
opt = {}
opt['data'] = None
opt['q'] = False

# Arguments
# ------------------------------------------------------------------------------

for arg in sys.argv[1:]:
    if arg == "-h":
        Help()
    elif arg == "-q":
        opt['q'] = True
    elif arg.endswith(".gz") or arg.endswith(".json"):
	if opt['data'] == None:
            opt['data'] = arg

# Utility functions
# ------------------------------------------------------------------------------

def openfile(filename):
    ''' opens the file and returns a reference to it '''
    if not filename:
        return sys.stdin
    elif filename.endswith(".gz"):
        return gzip.open(filename)
    else:
        return open(filename)

def debug(m):
    if not opt['q']:
        print >> sys.stderr, "Debug: %s"%m

# MAIN
# ------------------------------------------------------------------------------

if opt['data'] != None:
    allcontent = []
    debug( "Processing file: %s"% opt['data'] )
    f = openfile( opt['data'] )
    nline=0
    while True:
        nline+=1
        line = f.readline()
        if line == '':
            f.close() 
            break
        try:
            entry = json.loads(line)
        except:
            debug("Error in line: %d" % nline)
            debug(line)
            sys.exit(1)
        allcontent.append(entry)
    
    debug("sorting %d entries ..."% len(allcontent) ) 
    random.shuffle(allcontent)
    for entry in allcontent:
        print json.dumps(entry)

