#!/usr/bin/python
# -*- coding: utf-8 -*-

def Help():
    print >> sys.stderr, '''
================================================================================
Reads a file containing tagged examples, builds a model and applies it to events
Fernando Manuel Marques Batista  -  (c) Copyright 2014 -  Ver: 1.0 (unstable)
--------------------------------------------------------------------------------
Usage: %s [-h] [-v] [-scores] [-f=x] train.json[.gz] test.json[.gz]

options:
    -h : shows this help
    -q : low verbosity
    -scores: outputs the individual scores for all classes
    -f: minimum frequency of a word to be considered (default = 10)
'''%sys.argv[0]
    quit()

# Imports
# ------------------------------------------------------------------------------

import classifiers.tfidf as tc
import classifiers.tfidf2 as tc2
import re
import sys
import gzip
from text2tokens import *
import json

# Default values
# ------------------------------------------------------------------------------
opt = {}
opt['train'] = None
opt['test'] = None
opt['q'] = False
opt['scores'] = False
opt['f'] = 10

# Arguments
# ------------------------------------------------------------------------------

for arg in sys.argv[1:]:
    if arg == "-h":
        Help()
    elif arg == "-q":
        opt['q'] = True
    elif arg == "-scores":
        opt['scores'] = True
    elif arg.startswith("-f="):
        opt['f'] = float( arg.split("=")[1] )
    elif arg.endswith(".gz") or arg.endswith(".json"):
	if opt['train'] == None:
            opt['train'] = arg
        elif opt['test'] == None:
            opt['test'] = arg
    else:
        print >> sys.stderr, "error, unknown option: %s"%arg
        sys.exit(1)

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
fpc = tc.Classifier()
txt = text2tokens("./data/stopwords-en.txt")

# Process the training data
# --------------------------------------------------------------------------------
if opt['train'] != None:
    debug( "Processing file: %s"% opt['train'] )
    f = openfile( opt['train'] )
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
            debug("Error in line  %d" % nline)
            debug(line)
            sys.exit(1)

        fpc.add( entry["tag"], txt.process( entry["description"] ) )

# Information is now present. now performing all computations
# --------------------------------------------------------------------------------
fpc.createmodel( opt['f'] )

# Processing the testing data
# --------------------------------------------------------------------------------
if opt['test'] != None:
    debug( "Processing file: %s"% opt['test'] )
    f = openfile( opt['test'] )
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
            debug("Error in line  %d" % nline)
            debug(line)
            sys.exit(1)
	if fpc.knows_topic ( entry["tag"] ):
		scores = fpc.classify( entry["tag"], txt.process( entry["description"] ) )
		if opt["scores"]:
			print "%s\t%s"%(scores[0][0],", ".join(["%s %f"%(t,v) for t,v in scores]))
		else:
			print scores[0][0]
	else:
		print  >> sys.stderr, "Unknown tag ", tag
