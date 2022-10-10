#!/usr/bin/python
# -*- coding: utf-8 -*-

def Help():
    print >> sys.stderr, '''
================================================================================
Evaluates a classification hypothesis
Fernando Manuel Marques Batista  -  (c) Copyright 2014 -  Ver: 1.0 (unstable)
--------------------------------------------------------------------------------
Usage: %s [-h] [-v] [-cm] ref [hyp]

options:
    -h : shows this help
    -q : low verbosity
    -cm : shows the confusion matrix

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

# Default values
# ------------------------------------------------------------------------------
opt = {}
opt['ref'] = None
opt['hyp'] = None
opt['q'] = False
opt['cm'] = False

# Arguments
# ------------------------------------------------------------------------------

for arg in sys.argv[1:]:
    if arg == "-h":
        Help()
    elif arg == "-q":
        opt['q'] = True
    elif arg == "-cm":
        opt['cm'] = True
    elif opt['ref'] == None:
        opt['ref'] = arg
    elif opt['hyp'] == None:
        opt['hyp'] = arg

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

# --------------------------------------------------------------------------------
if opt['ref'] != None:
	f = openfile(opt['ref'])
        ref = [ line.strip().split("\t")[0] for line in f ]
	f.close()
else:
	sys.exit(1)

f = openfile(opt['hyp'])
hyp = [ line.strip().split("\t")[0] for line in f ]
f.close()

if len(ref) != len(hyp):
    debug("Error: different lenghts")
    sys.exit(1)

cm = collections.Counter()
performance = collections.Counter()
for i in range(len(ref)):
    if opt["cm"]: cm[(ref[i],hyp[i])] += 1 
    if ref[i] == hyp[i]:
          performance['cor'] += 1
          performance[ref[i]+'.cor'] += 1
    else:
          performance['inc'] += 1
          performance[ref[i]+'.inc'] += 1
print "Correct %d/%d, ACCURACY: %f"% ( performance['cor'], performance['cor']+performance['inc'], float( performance['cor']) / (performance['cor']+performance['inc']) )

if opt["cm"]:
    #clist = ["software", "web", "ecommerce", "games_video", "mobile", "advertising", "biotech", "consulting", "enterprise", "education", "hardware", "health", "public_relations", "network_hosting", "finance", "cleantech", "search", "social", "local", "analytics", "medical", "security", "travel", "manufacturing", "legal", "news", "hospitality", "fashion", "sports", "real_estate", "semiconductor", "photo_video", "music", "transportation", "automotive", "messaging", "design", "nonprofit", "pets", "nanotech", "government", "other"]
    clist = [x for (x,c) in sorted(collections.Counter(ref).iteritems(), key=operator.itemgetter(1), reverse=True)]
    print "classified_as_=>", " ".join(clist)
    for r in clist:
        line = [r]
        for h in clist:
           line.append( str(cm[(r,h)]) )
        print " ".join(line)













