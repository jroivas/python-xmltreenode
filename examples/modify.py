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
root = res.getRoot()

root.addAttrib('added_attribute', 'Hello')

index = 0
renamed = None
last = None
for item in root:
    if index == 1:
        item.setData('renamed_tag')
        renamed = item
    last = item
    index += 1

if renamed is not None:
    new_item = xmltreenode.XMLTreeNode("new_item")
    new_item_0 = xmltreenode.XMLTreeNode("new_item_at_0")
    renamed.addChild(new_item)
    renamed.insertChild(0, new_item_0)

if last is not None and last != renamed:
    root.removeChild(last)

print (root.toString())
