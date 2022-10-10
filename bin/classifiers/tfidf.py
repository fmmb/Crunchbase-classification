#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import math
import operator
import collections

def tfidf(tf_t_d, ndocs, df_t):
    '''
	tf_t_d: frequency of term t in document d
	ndocs : number of different documents
	df_t: number of documents that contain t
    '''
    if tf_t_d > 0:
	#return (1.0 + math.log(tf_t_d) ) * math.log(ndocs/df_t,10)
	return tf_t_d * math.log((ndocs+1)/df_t,10)  # SMOOTHED VERSION
    else:
	return 0

class topic_model:
    def __init__(self):
	self.wc = collections.Counter()
	self.tfidf= {}
        self.topk=[]

    def add(self, text):
	for w in text:
	    self.wc[w] += 1

    def set_tfidf(self, w, N, df_w):
	v = tfidf( self.wc[w], N, df_w)
	if v > 0: self.tfidf[w] = v

    def similarity(self, words):
	res = 0.0
	for w in words:
	   if self.tfidf.has_key(w):
	      res += self.tfidf[w]
	return res

    def freqwords(self, minfreq=1):
	res=[]
	for k in self.wc.iterkeys():
	    if self.wc[k] >= minfreq:
		res.append(k) 
	return res

    def set_relevant_words(self):
        #self.topk = [ w for (w,v) in sorted(self.wc.iteritems(), key=operator.itemgetter(1), reverse=True) ]
        self.topk = [ w for (w,v) in sorted(self.tfidf.iteritems(), key=operator.itemgetter(1), reverse=True) ]

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
	df = collections.Counter() 
	for t in self.topics:
	    for w in self.tm[t].freqwords(minfreq):
	        df[w] += 1

	for t in self.topics:
	    for w in self.tm[t].freqwords(minfreq):
    	        self.tm[t].set_tfidf(w, len(self.topics), df[w] )
            self.tm[t].set_relevant_words()
            #print >> sys.stderr, "==>",t
            #for w in self.tm[t].topk[:100]:
            #    print >> sys.stderr, "(%s, %d, %d, %f)"%(w.encode("utf-8"), self.tm[t].wc[w], df[w], self.tm[t].tfidf[w]),
            #print >> sys.stderr, ""

    def get_sorted_relevant_words(self):
        # for each word, computes the number of documents in which it occurs
        relwords = {}
        for t in self.topics:
            for (w,v) in self.tm[t].relevant_words():
                if relwords.has_key(w):
                    relwords[w] = max(relwords[w], v )
                else:
                    relwords[w] = v

        return sorted(relwords.iteritems(), key=operator.itemgetter(1), reverse=True)

    def knows_topic(self, topic):
        return topic in self.topics

    def classify(self, topic, words):
        ''' Assumes that "words" is a list of words '''
        scores = [ (t, self.tm[t].similarity(words)) for t in self.topics ]
        scores = sorted(scores,key=operator.itemgetter(1),reverse=True)
        return scores

if __name__=='__main__':
	c = Classifier()
	train=[]
	test=[]
	train.append( ["pt", "eu sou o maior do mundo"] )
	train.append( ["en", "the best in the west"] )
	train.append( ["pt", "o maior centro do mundo"] )
	train.append( ["en", "in the best of the best"] )
	test.append( ["pt", "o manuel é o maior do planeta"] )
	test.append( ["en", "do your best is always the way"] )
	test.append( ["pt", "quem diz o que não sabe"] )
	test.append( ["en", "can you be in the park ?"] )
	for (t,s) in train:
	   c.add( t, s.split() )
		
	c.createmodel(1)

	for (t,s) in test:
		if c.knows_topic(t):
			scores = c.classify(t, s.split() )
			print scores[0][0], scores, "#", s

		else:
			print  >> sys.stderr, "Unknown tag ", t


