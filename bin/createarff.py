#!/usr/bin/python
# -*- coding: utf-8 -*-

def Help():
    print >> sys.stderr, '''
================================================================================
Reads a file containing tagged examples, builds a model and applies it to events
Fernando Manuel Marques Batista  -  (c) Copyright 2014 -  Ver: 1.0 (unstable)
--------------------------------------------------------------------------------
Usage: %s [-h] [-v] attribs.txt [file.arff[.gz]] data.json[.gz]

options:
    -h : shows this help
    -q : low verbosity
    file.arff: will be used to provide the header and the list of attributes
    attribs.txt: file containing a list of selected attributes (words)

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
from text2tokens import *
import json

# Default values
# ------------------------------------------------------------------------------
opt = {}
opt['data'] = None
opt['q'] = False
opt['att'] = None
opt['arff'] = None

# Arguments
# ------------------------------------------------------------------------------

for arg in sys.argv[1:]:
    if arg == "-h":
        Help()
    elif arg == "-q":
        opt['q'] = True
    elif arg.endswith("json.gz") or arg.endswith(".json"):
        opt['data'] = arg
    elif arg.endswith("arff.gz") or arg.endswith(".arff"):
        opt['arff'] = arg
    elif arg.endswith(".txt"):
        opt['att'] = arg

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

class vocabulary():
    def __init__(self, fname):
        self.excl_chars = re.compile(ur'[\u00e2\u00c2\u00c3]', re.UNICODE)
    	self.attribute={}
	self.classes=[]
	self.total = -1
        #if fname.endswith("arff") or fname.endswith("arff.gz"): 
        #    self.parse_arff(fname)
        #else:
	self.parse_wordlist(fname)

    def parse_wordlist(self, fname):
	f = openfile(fname)
	for w in f:
            if self.excl_chars.search(w):
                debug("skipping word with strange chars in vocabulary: %s"% w.strip() )
	    elif not self.attribute.has_key( w.strip() ):
		self.total += 1
		self.attribute[w.strip()] = self.total
	f.close()

    def parse_arff(self, fname):
	f = openfile(fname)
	for line in f:
            if line.startswith("@attribute "):
                self.total += 1
                self.attribute[ line.split(" ")[1].strip('"\'') ] = self.total
            if line.startswith("@data"):
                break
	f.close()

    def numclass(self):
	return self.total + 1

    def arffheader(self):
	print '@relation topic_det'
	sattribs=sorted(self.attribute.iteritems(),key=operator.itemgetter(1),reverse=False)
	for (t,v) in sattribs:
	    print "@attribute \"%s\" numeric"%(t)
	print '@attribute Category {"%s"}'% ('","'.join(self.classes))

    def todata(self, tag, words, newattribs=False):
	if tag not in self.classes:
	    self.classes.append(tag)
	res=collections.Counter()
	for w in words:
	    if newattribs and not self.attribute.has_key(w):
		self.total += 1
		self.attribute[w] = self.total
            if self.excl_chars.search(w):
                debug("skipping word with strange chars: %s"% w.encode("utf-8") )
            elif self.attribute.has_key(w): 
	        res[self.attribute[w]] += 1
	return (res,tag)

# MAIN
# ------------------------------------------------------------------------------
if not opt['att']:
    print >> sys.stderr, "Error, please specify the list of attributes. example: ./data/most-relevant-words.txt"
    sys.exit(1)

voc = vocabulary(opt['att']) 
txt = text2tokens("./data/stopwords-en.txt")
data_trn = []

# Process the training data
# --------------------------------------------------------------------------------
if opt['data'] != None:
    debug( "Processing file: %s"% opt['data'] )
    f = openfile( opt['data'] )
    for nline, line in enumerate(f):
        try:
            entry = json.loads(line.strip())
        except:
            debug("error in line %d: %s" % (nline, line) )
            sys.exit(1)

        data_trn.append( voc.todata( entry["tag"], txt.process( entry["description"] ) ) )
    f.close()

if opt['arff']:
    f = openfile(opt['arff'])
    for line in f:
        print line,
        if line.startswith("@data"): break
    f.close()
else:
    voc.arffheader()
    print "@data"

for (v,t) in data_trn:
   sv = sorted(v.iteritems(), key=operator.itemgetter(0), reverse=False)
   sv.append( (voc.numclass(), '"%s"'%t) )
   print '{%s}'%(", ".join(["%d %s"%(a,c) for (a,c) in sv] ))


