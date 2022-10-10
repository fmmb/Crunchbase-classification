#!/usr/bin/python
# -*- coding: utf-8 -*-

def Help():
    print >> sys.stderr, '''
================================================================================
Reads a file containing tagged examples and extracts usefull info
Fernando Manuel Marques Batista  -  (c) Copyright 2014 -  Ver: 1.0 (unstable)
--------------------------------------------------------------------------------
Usage: %s [-h] [-v] data.json[.gz]

options:
    -h : shows this help
    -q : low verbosity
    -tfidf : outputs the most relevant words based of tf-idf

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

#allowedtags=["other", "software", "web", "ecommerce", "games_video", "mobile", "advertising", "biotech", "consulting", "enterprise", "education", "hardware", "health", "public_relations", "network_hosting", "finance", "cleantech", "search", "social", "local", "analytics", "medical", "security", "travel", "manufacturing", "legal", "news", "hospitality", "fashion", "sports", "real_estate", "semiconductor", "photo_video", "music", "transportation", "automotive", "messaging", "design", "nonprofit", "pets", "nanotech", "government"]
#allowedtags=["other", "software", "web", "ecommerce", "games_video", "mobile", "advertising", "biotech", "consulting", "enterprise", "education", "hardware", "health"]
#allowedtags+=["public_relations", "network_hosting", "finance", "cleantech", "search", "social", "local", "analytics", "medical", "security", "travel", "manufacturing"]
discardtags=["other"]

# Process the data
# --------------------------------------------------------------------------------
if opt['data'] != None:
    debug( "Processing file: %s"% opt['data'] )

    f = openfile( opt['data'] )
    for nline, line in enumerate(f):
        try:
            entry = json.loads(line)
        except:
            debug("Error in line  %d" % nline)
            debug(line)
            sys.exit(1)

        if entry['tag'] not in discardtags:
            print line,
        #if entry['tag'] in allowedtags:
        #    print line,
        #else:
        #    entry['tag']='other'
        #    print json.dumps(entry)
    f.close()
