#!/usr/bin/python
# -*- coding: utf-8 -*-

def Help():
    print >> sys.stderr, '''
================================================================================
Reads a file containing tagged examples and extracts usefull info
Fernando Manuel Marques Batista  -  (c) Copyright 2014 -  Ver: 1.0 (unstable)
--------------------------------------------------------------------------------
Usage: %s [-h] [-v] data.json[.gz] [ -tfidf | -tag | -description | -wordfreq | -desclen ]

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
from text2tokens import *
import json

# Default values
# ------------------------------------------------------------------------------
opt = {}
opt['data'] = None
opt['q'] = False
opt['tfidf'] = False
opt['tag'] = False
opt['description'] = False
opt['desclen'] = False
opt['wordfreq'] = False

# Arguments
# ------------------------------------------------------------------------------

for arg in sys.argv[1:]:
    if arg == "-h":
        Help()
    elif arg in ["-q", "-tag", "-description", "-desclen", "-wordfreq", "-tfidf"]:
        opt[ arg[1:] ] = True
    elif arg.endswith(".gz") or arg.endswith(".txt"):
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

def tfidf(tf_t_d, ndocs, df_t):
    '''
        tf_t_d: frequency of term t in document d
        ndocs : number of different documents
        df_t: number of documents that contain t
    '''
    if tf_t_d > 0:
        #return (1.0 + math.log(tf_t_d) ) * math.log(float(ndocs)/df_t,10)
        return tf_t_d * math.log((ndocs+1.0)/df_t,10)  # SMOOTHED VERSION
    else:
        return 0

class topic_model:
    def __init__(self):
        self.wc = collections.Counter()
        self.tfidf= {}

    def add(self, text):
        for w in text:
            self.wc[w] += 1

    def set_tfidf(self, w, N, df_w):
        v = tfidf( self.wc[w], N, df_w)
        if v > 0: self.tfidf[w] = v

    def freqwords(self, minfreq=1):
        res=[]
        for k in self.wc.iterkeys():
            if self.wc[k] >= minfreq:
                res.append(k)
        return res

    def relevant_words(self):
        return sorted(self.tfidf.iteritems(), key=operator.itemgetter(1), reverse=True)

class Classifier:
    def __init__(self):
        self.topics = set([])
        self.tm = { t:topic_model() for t in self.topics }

    def add(self, topic, words ):
        ''' Updates the words for the correspondic set of topics '''
        if topic not in self.topics:
            self.topics.add(topic)
            self.tm[topic] = topic_model()
        self.tm[topic].add( words )

    def createmodel(self, minfreq):
        # for each word, computes the number of documents in which it occurs
        self.df = collections.Counter()
        for t in self.topics:
            for w in self.tm[t].freqwords(minfreq):
                self.df[w] += 1

        for t in self.topics:
            for w in self.tm[t].freqwords(minfreq):
                self.tm[t].set_tfidf(w, len(self.topics), self.df[w] )

    def print_sorted_relevant_words(self):
        # for each word, computes the number of documents in which it occurs
        relwords = {}
        for t in self.topics:
            for (w,v) in self.tm[t].relevant_words():
                if relwords.has_key(w):
                    relwords[w] = max(relwords[w], v )
                else:
                    relwords[w] = v
        for (w,v) in sorted(relwords.iteritems(), key=operator.itemgetter(1), reverse=True):
            print w.encode("utf-8"), self.df[w], v

# MAIN
# ------------------------------------------------------------------------------

if opt["wordfreq"]:
    wc = collections.Counter()
if opt['tfidf']:
    fpc = Classifier()

txt = text2tokens()

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

        if opt['tag']:
                print entry["tag"].encode("utf-8")
        elif opt['description']:
                print entry["description"].encode("utf-8")
        elif opt['desclen']:
                print entry["tag"], len(txt.process( entry["description"] ))
        elif opt['wordfreq']:
                for i in txt.process( entry["description"] ):
                   wc[i] += 1
        elif opt['tfidf']:
                fpc.add( entry["tag"], txt.process( entry["description"] ) )
        else:
            print "COMPANY:", entry['company']
            print "TAG:", entry['tag']
            print entry["description"], "\n"
    f.close()

if opt["wordfreq"]:
   for (w,v) in sorted(wc.iteritems(), key=operator.itemgetter(1), reverse=True):
	print w.encode("utf-8"), v
elif opt['tfidf']:
    fpc.createmodel(minfreq=3)
    fpc.print_sorted_relevant_words()

