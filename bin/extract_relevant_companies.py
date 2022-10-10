#!/usr/bin/python
# -*- coding: utf-8 -*-

def Help():
    print >> sys.stderr, '''
================================================================================
Reads a file where each line is a json string a prints the corresponding info
Fernando Manuel Marques Batista  -  (c) Copyright 2014 -  Ver: 1.0 (unstable)
--------------------------------------------------------------------------------
Usage: %s [-h] [-q] [-mw=x] [-en] [-txt] info.txt[.gz]

options:
    -h : shows this help
    -q : low verbosity
    -mw : Minimum number of words that the entity overview should contain
    -en : removes lines containing content from languages different than english
    -txt: writes the output in text format instead of json

'''%sys.argv[0]
    quit()


import sys
import json
import time
import re
import gzip

# Default values
# ------------------------------------------------------------------------------
opt = {}
opt['filename'] = None
opt['q'] = False
opt['mw'] = 0 
opt['en'] = False 
opt["txt"] = False

excl_chars = re.compile(ur'[\u0400-\u2000\u3000-\uffff]', re.UNICODE)

# Arguments
# ------------------------------------------------------------------------------
for arg in sys.argv[1:]:
    if arg == "-h":
        Help()
    elif arg == "-q":
        opt['q'] = True
    elif arg == "-en":
        opt['en'] = True
    elif arg == "-txt":
        opt['txt'] = True
    elif arg.startswith("-mw"):
        opt['mw'] = int(arg.split("=")[1])
    elif arg.endswith(".gz") or arg.endswith(".json"):
        opt['filename'] = arg
    else:
        Help()

# Utility functions
# ------------------------------------------------------------------------------

def openfile(filename):
    '''
    opens the file and returns a reference to it
    '''
    if not filename:
        return sys.stdin
    elif filename.endswith(".gz"):
        return gzip.open(filename)
    else:
        return open(filename)

def debug(m):
    if not opt['q']:
        print >> sys.stderr, "Debug: %s"%m

def not_english( text ):
    if excl_chars.search(text):
        return True
    elif re.search(" (ist|la|le|des|da|e|su|je|en|o|y|con) ", text ):
        return True
    else:
        return False

if __name__ == '__main__':
    f = openfile ( opt['filename'])
    linha = f.readline()
    while linha != '':
        try:
            entity = json.loads(eval(linha))
        except:
            debug( "Warning, could not parse line: %s"%(linha) )
            entity = {}
        if entity.has_key("category_code") and entity.has_key("overview"):
            if entity["category_code"] != None and entity["overview"] != None:
                overview = re.sub(r"<[\/a-z]+>", "", entity["overview"] )
                overview = re.sub(r"  +", "", overview).strip()
                if opt["mw"] > len(overview.split() ):
                    debug("Skipping company: %s, tag: %s, desc=%s"%(
                        entity["name"].encode("utf-8").strip(), entity["category_code"].encode("utf-8"), overview.encode("utf-8") ) )
                elif opt["en"] and not_english(overview):
                    debug("Warning: discarding content (unknown chars or other language): %s" % overview.encode("utf-8") )
		elif opt["txt"]:
                    print "COMPANY:", entity["name"].encode("utf-8").strip()
                    print "TAG:", entity["category_code"].encode("utf-8")
                    print overview.encode("utf-8")
                    print
                else:
                    company = entity["name"].encode("utf-8").strip()
                    tag = entity["category_code"].encode("utf-8")
                    description = overview.encode("utf-8")
                    print json.dumps({"company": company, "tag": tag, "description": description})
        linha = f.readline()
    f.close()

