#!/usr/bin/python
# -*- coding: utf-8 -*-

# This version is similar to the version used for twiter classification

import sys
import math
import operator
import collections

class FuzzyFunction:
    def __init__(self, k, ftype=None):
        self.k = k
        if ftype == None or ftype == 'pareto':
            self.f = self.fmiu_pareto
        elif ftype == 'erfc':
            self.f = self.fmiu_erfc
        else:
           raise Exception("Error, unknown function: "%ftype)

    def value(self, i):
        if i < self.k:
            return self.f(i)

    def fmiu_erfc(self, i):
        return 1.0-math.erf(2.0*float(i)/self.k)

    def fmiu_pareto(self, i):
        a=float(0.2*self.k)
        b=float(0.2)
        if i<a:
            return 1-(1-b)*(i/float(self.k*b))
        else:
            return a*(1-float(i-a)/float(self.k-a))/float(self.k)

def itf(noccur, ntopics):
    return  math.log((ntopics+1)/float(noccur),10)

class fingerprint:
    ''' fingerprint class '''
    def __init__(self):
	self.wc = collections.Counter()
	self.topk = None

    def add(self, text):
	for w in text:
	    self.wc[w] += 1

    def setfp(self, topk, ff):
	''' final step, where the fingerprint is set '''
        self.topk = {}
        i = 0
        for (w,v) in sorted(topk, key=operator.itemgetter(1), reverse=True):
            self.topk[w] = ff.value(i)
            i += 1

    def similarity(self, tw_wlist):
	sim = 0.0
	for w in tw_wlist:   # BETTER RESULTS IF SET IS REMOVED
	    if w in self.topk:
		sim += self.topk[w]
	return float(sim)

    def freqwords(self, n=None):
	if n != None:
	    return sorted(self.wc.iteritems(), key=operator.itemgetter(1), reverse=True)[:n]
	else:
	    return sorted(self.wc.iteritems(), key=operator.itemgetter(1), reverse=True)

class Classifier:
    ''' fingerprints-based classifier '''

    def __init__(self):
	self.topics = set([]) 
	self.fp = { t:fingerprint() for t in self.topics }
	
    def add(self, topic, words ):
        ''' Updates the words for the correspondic set of topics '''
	if topic not in self.topics:
	    self.topics.add(topic)
	    self.fp[topic] = fingerprint()
	self.fp[topic].add( words ) 

    def createmodel(self, K):
	''' creates the model using the K most relevant words'''
        ff = FuzzyFunction(K, 'pareto')

	tf = collections.Counter() 
	for t in self.topics:
	    for (w,f) in self.fp[t].freqwords(K):
	       tf[w] += 1

	for t in self.topics:
            topk = [ (w, f * itf(tf[w], len(self.topics)) ) for (w,f) in self.fp[t].freqwords(K) ]
	    self.fp[t].setfp(topk, ff)

    def knows_topic(self, topic):
	return topic in self.topics

    def classify(self, topic, words):
	''' Assumes that "words" is a list of words '''

	scores = [ (t, self.fp[t].similarity( words ) ) for t in self.topics ] 
	scores = sorted(scores,key=operator.itemgetter(1),reverse=True)
	return scores

if __name__=='__main__':
        c = Classifier()
        train=[]
        test=[]
        train.append( ["pt", "eu sou o maior do mundo"] )
        train.append( ["en", "the best in the west"] )
        train.append( ["pt", "o maior centro do mundo no"] )
        train.append( ["en", "no in the best of the best"] )
        test.append( ["pt", "o manuel é o maior do planeta"] )
        test.append( ["en", "do your best is always the way"] )
        test.append( ["pt", "quem diz o que não sabe"] )
        test.append( ["en", "can you be in the park ?"] )
        for (t,s) in train:
           c.add( t, s.split() )

        c.createmodel(10)

        for (t,s) in test:
                if c.knows_topic(t):
                        scores = c.classify(t, s.split() )
                        print scores[0][0], scores, "#", s

                else:
                        print  >> sys.stderr, "Unknown tag ", t

