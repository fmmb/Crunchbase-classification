#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

def openfile(filename):
    ''' opens the file and returns a reference to it '''
    if not filename:
        return sys.stdin
    elif filename.endswith(".gz"):
        return gzip.open(filename)
    else:
        return open(filename)

class text2tokens:
    ''' stop-words class '''
    def __init__(self, fname = None):
        self.sw = set([])
	if fname != None: self.parse(fname)
        self.excl_chars = re.compile(ur'[\u0400-\u2000\u3000-\uffff]', re.UNICODE)

    def parse(self, fname):
        f = openfile(fname)
        for line in f.readlines():
            self.sw.add( line.strip() )
        f.close()

    def filter(self, words):
        res = []
        for w in words:
           if ( w.lower() not in self.sw ) and (len(w) > 1):
              res.append(w)
        return res

    def process(self, text):
	while True:
	    ptext = text
            text = re.sub(r"[0-9]+,[0-9]+,[0-9]+","_numM_",text)  
            text = re.sub(r"[0-9]+,[0-9]+","_numK_",text)  
            text = re.sub(r"[\,\.?]( |$)"," ",text)
            text = re.sub(r"[;:)\]]"," ",text)  # solution,sales
            text = re.sub(r"(^| )[(\[]"," ",text)
            text = re.sub(r'[\\"]',"",text)
	    if ptext == text: break

        words = []
        for w in text.strip().split():
            if self.excl_chars.search(w):
                pass
            elif w.istitle():
                words.append(w.lower())
            elif w.isdigit():
                pass
            elif w in self.sw: 
                pass
            else:
                words.append(w)
        if len(self.sw) > 0:
            return self.filter(words)
        else:
            return words

if __name__=='__main__':
    t2t = text2tokens("./data/stopwords-en.txt")
    print t2t.process("(a) the patients suffering from a disease were cured from their cancer. that is good.")
    t2t = text2tokens()
    print t2t.process("(a) the patients suffering from a disease were cured from their cancer. that is good.")
    print t2t.process("linux, and ,windows and solution,sales spent 1000,000 dollars")

