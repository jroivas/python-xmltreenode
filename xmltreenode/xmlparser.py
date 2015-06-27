"""@package xmlparser
Primary XML parsing interface as well some other misc support functionality
"""

from __future__ import print_function
from xmltreenode import XMLTreeNode
from xml.etree.ElementTree import Comment
from xml.etree.ElementTree import XMLParser


class CommentParser(XMLParser):
    """Special class to handle comment parsing
    """

    def __init__(self, target=None):
        """Initialize
        @param target Target class
        """
        from xml.etree.ElementTree import XMLTreeBuilder
        XMLTreeBuilder.__init__(self, html=0, target=target)
        self._parser.CommentHandler = self.comment

    def comment(self, data):
        """Get comment data and add it to the tree

        @param data Data to be added as comment
        """
        self._target.start(Comment, {})
        self._target.data(data)
        self._target.end(Comment)

use_cetree = True
if use_cetree:
    import sys
    if sys.version >= '3.3':
        from xml.etree.ElementTree import ParseError
        from xml.etree.ElementTree import XMLParser
    else:
        from xml.etree.cElementTree import ParseError  # NOQA
        from xml.etree.cElementTree import XMLParser  # NOQA
    xml_parser = XMLParser
else:
    from xml.etree.ElementTree import ParseError  # NOQA
    xml_parser = CommentParser


class CustomXMLParser():
    """Special class meant to use with XMLParser to get walkthrough of the XML parse tree
    Will create tree presentation of XML file utilizing the XMLTreeNode class.
    """

    def __init__(self, parseSpecial=True):
        """Initialize

        @param parseSpecial If True, will parse and handle special tags. If you need only bare parsing, set this to False
        """
        self.__name = ""
        self.__node = None
        self.__root = None
        self.__tagname = None
        self.__rootcomments = []

        self.__ignore_errors = False

    def ignoreErrors(self, val):
        self.__ignore_errors = val

    def __getitem__(self, index):
        """ Get item

        @param index Index of item
        @returns XMLTreeNode
        """
        if self.__root is None:
            return None

        return self.__root[index]

    def __contains__(self, index):
        """ Does it contain an item

        @param index Item
        @returns True if found, False otherwise
        """
        if self.__root is None:
            return False

        return index in self.__root

    def __len__(self):
        """ Length or number of items

        @return Number of items
        """
        if self.__root is None:
            return 0

        return len(self.__root)

    def getRoot(self):
        """Return root node of the generated tree

        @returns Root node of the generated tree or None
        """
        return self.__root

    def startHandleTag(self):
        """ Handle normal tag, just create new XMLTreeNode and set it as child to current node or make it the root node

        """
        # Just a normal, non-empty tag, so create tree node
        node = XMLTreeNode(self.__name)

        if self.__node is not None:
            self.__node.addChild(node)
        else:
            # We do not have current node which means we do not
            # have a root node yet, so this is the one
            self.__root = node
            for c in self.__rootcomments:
                self.__root.addChild(c)
            self.__rootcomments = []

        # Mark current node
        self.__node = node

    def comment(self, data):
        """Get comment data and add it to the tree
        """
        self.start(Comment, {})
        self.data(data)
        self.end(Comment)

    def start(self, tag, attrib):
        """This is called when a start tag is found from XML

        @param tag Tag name
        @param attrib Attributes
        """
        if tag == Comment:
            self.__name = tag

            node = XMLTreeNode(Comment)
            if self.__node is not None:
                self.__node.addChild(node)
            elif self.__root is None:
                self.__rootcomments.append(node)

            self.__node = node
            return

        self.__name = tag.strip()
        self.__tagname = None

        if self.__name:
            self.startHandleTag()

        # Check if there's attributes and create a tree structure out of them
        if attrib:
            for attr in attrib:
                self.__node.addAttrib(attr, attrib[attr])

    def end(self, tag):
        """The end of the tag, handle properly, free what needs to be freed

        @param data Tag data
        """
        if tag == Comment:
            if self.__node is None:
                return
            par = self.__node.getParent()
            if par is not None:
                self.__node = par
            if self.__root is None:
                self.__node = None
            return

        tag = tag.strip()
        if tag and self.__node is not None:
            # Walk down to the tree if possible (towards the root)
            par = self.__node.getParent()
            if par is not None:
                self.__node = par

    def data(self, data):
        """The data/contents of the tag

        @param data Tag data
        """
        ___name = self.__name

        # First handle comments
        if ___name == Comment:
            if data and self.__node is not None:
                self.__node.appendValue(data)
            return

        if len(data.strip()) > 0 and ___name:
            # And create the value node
            self.__node.appendValue(data)

    def close(self):
        """Called when parsing/parser is closed
        """
        return

    def loadFile(self, xmlfile, sourceIsFile):
        """ Load and parse a XML file

        @param xmlfile Input XML file
        @param sourceIsFile Set this True if xmlfile parameter is a file, False if it contains XML content as a string
        @returns Parsed XML file or None
        """
        curxml = None
        if sourceIsFile:
            # We have a file so try to read
            try:
                f = open(xmlfile, "r")
                contents = f.read()
                f.close()
            except IOError:
                tmp = "File %s not found!" % xmlfile
                if self.__ignore_errors:
                    print ("ERROR: %s" % tmp)
                    return None
                else:
                    raise ValueError(tmp)
            curxml = contents
        else:
            curxml = xmlfile

        return curxml

    def load(self, xmlfile, sourceIsFile=True, addDummy=False):
        """Load XML file or raw text
        xmlfile is either name of the XML file
        or contents of XML data in case of sourceIsFile=False

        @param xmlfile Input XML file
        @param sourceIsFile Set this True if xmlfile parameter is a file, False if it contains XML content as a string
        @param addDummy Add given xml file contents to into dummy element, <dummy> xmlfile </dummy>
        @returns CustomXMLParser instance containing the loaded file OR list of XMLTreeNode instances containing tag elements in case multiple root tags found
        """
        if xmlfile is None:
            return self

        curxml = self.loadFile(xmlfile, sourceIsFile)
        if curxml is None:
            return None

        if addDummy:
            curxml = '<dummy>\n' + curxml + '\n</dummy>'

        # And feed the XML to parser with the this custom parser walker
        parser = xml_parser(target=self)

        reraise = False
        err = None
        try:
            parser.feed(curxml)
            parser.close()
        except ParseError as e:
            reraise = True
            err = e

        if reraise:
            if sourceIsFile:
                raise ValueError('Input is not valid XML: %s, %s' % (xmlfile, err))
            else:
                raise ValueError('Input is not valid XML: %s' % err)

        # Parse the dummy from under the root
        if addDummy:
            c = self.__root.getChildren()
            for dd in c:
                if dd.getData() == 'dummy':
                    self.__root = dd

        # Return ourself when success
        return self

# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
