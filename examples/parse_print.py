#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "xmltreenode"))
sys.path.append(os.path.dirname(__file__))

import xmltreenode

if len(sys.argv) <= 1:
    print ('Usage: %s file.xml' % (sys.argv[0]))
    sys.exit(1)

parse = xmltreenode.CustomXMLParser()
res = parse.load(sys.argv[1])
print (res.getRoot().toString())
