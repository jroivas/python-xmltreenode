"""@package xmltreenode
Has class for special XMLTreeNode for parse tree presentation
"""

from __future__ import print_function
import copy
import sys
import xml.etree.ElementTree

use_cetree = True
if use_cetree:
    if sys.version >= '3.3':
        element_tree = xml.etree.ElementTree
    else:
        import xml.etree.cElementTree
        element_tree = xml.etree.cElementTree
else:
    element_tree = xml.etree.ElementTree


class XMLTreeNode(object):
    """ Custom Tree structure, may contain any number of children.
    XMLTreeNode can contain about any value or data,
    any number of children and subchildren.
    Contains definations and parsing capabilities.
    """
    def __init__(self, tag=None, attrib={}, **extra):
        """ Initialize

        @param tag Setup the data of this node, can be overridden later with setData
        @param attrib Element attribute dictionary
        @param **extra Additional attributes, given as keyword arguments
        """
        self.tag = tag
        self.attrib = attrib.copy()
        self.attrib.update(extra)
        self._children = []

        self.text = ''
        self.tail = ''

        self.__parent = None
        self.__nodeType = None

    def deepcopy(self):
        """ Copy this XMLTreeNode. Makes sure everything needed will be copied.

        @returns New XMLTreeNode which is copy of the current
        """
        # Custom solution to ensure few things
        tmp = XMLTreeNode()
        tmp.__nodeType = self.__nodeType
        tmp.text = self.text
        tmp.tag = self.tag
        tmp.__parent = None
        tmp.attrib = self.attrib.copy()

        for c in self._children:
            newch = c.deepcopy()
            tmp.addChild(newch)

        return tmp

    def copy(self):
        """ Copy this XMLTreeNode. Makes sure everything needed will be copied.

        @returns New XMLTreeNode which is copy of the current
        """
        # Let's do a little bit deeper copy, but not that deep
        tmp = copy.copy(self)
        tmp.attrib = self.attrib.copy()
        tmp.__parent = None
        return tmp

    def setValue(self, value):
        """ Set value of the Node, or the text

        @param value Any value
        """
        self.text = value

    def getValue(self):
        """ Return value of the XMLTreeNode

        @returns Value of the XMLTreeNode
        """
        return self.text

    def appendValue(self, value):
        """ Set value of the Node, or the text

        @param value Any value
        """
        self.text = "%s%s" % (self.text, value)

    def insertAfterChild(self, afterchild, child, reparent=True):
        """ Add a child node after another child

        @param afterchild Child instance to be before the new child
        @param child Any instance of XMLTreeNode
        @param reparent True if should be reparented, False to skip
        """
        if reparent:
            child.reparent(self, addchild=False)

        chs = self._children
        if child not in chs:
            try:
                pos = self._children.index(afterchild)
                self.insert(pos + 1, child)
            except:
                self.append(child)

    def insertChild(self, index, child, reparent=True):
        """ Insert child at specific position

        @param index Index in the list where to insert
        @param child Any instance of XMLTreeNode
        @param reparent True if should be reparented, False to skip
        """
        if reparent:
            child.reparent(self, addchild=False)

        if child not in self._children:
            self._children.insert(index, child)

    def addChild(self, child, reparent=True):
        """ Add a child node, need to be instance of XMLTreeNode

        @param child Any instance of XMLTreeNode
        @param reparent True if should be reparented, False to skip
        """
        if reparent:
            # This will call addChild again after reparenting is done
            # but reparent flags as False
            # This way it's safe to assume we just call reparent
            # and do nothing else here.
            child.reparent(self, addchild=False)

        if child not in self._children:
            # If we don't have the reparent flag then do the real add...
            # Prevent adding if already there
            self._children.append(child)

    def append(self, item):
        """ Append item to XMLTreeNode structure, uses addChild to add item as a new child

        @param item Item to be appended
        """
        self.addChild(item)

    def insert(self, pos, item):
        """ Insert item to given position in the XMLTreeNode structure, uses insertChild

        @param pos Position where to insert
        @param item Item to be added
        """
        self.insertChild(pos, item)

    def remove(self, item):
        """ Remove item from the XMLTreeNode structure

        @param item Item to be removed
        """
        self.removeChild(item)

    def __len__(self):
        """ Return the length of XMLTreeNode instance, amount of children.

        @returns Length of the XMLTreeNode structure, number of children
        """
        return len(self._children)

    def finditer(self, name):
        """ Find iterative data which has given name as tag

        @param name Name of searched iter item
        @returns Item which matches the searched name
        """
        for item in self._children:
            if item.tag == name:
                yield item

    def findall(self, name):
        """ Find all items matching the given name

        @param name Name to search
        @returns List of items corresponding the searched name
        """
        return list(self.finditer(name))

    def iter(self, tag=None):
        """ Return a Iterator object

        @param tag Tag name
        @returns Iterator object matched for searched tag
        """
        if tag == '*':
            tag = None
        if tag is None or self.tag == tag:
            yield self
        for ch in self._children:
            for e in ch.iter(tag):
                yield e

    def items(self):
        """ Get all attribute items

        @returns List of all attribute items
        """
        return self.attrib.items()

    def numChildren(self):
        """ Return the number of children under this XMLTreeNode

        @returns Number of children
        """
        return len(self._children)

    def getChildren(self):
        """ Get list of children

        @returns List of all children under this XMLTreeNode
        """
        # Make copy of the list to prevent weird
        # reference manipulating errors...
        return self._children[:]

    def getChildrenRef(self):
        """ Get list of children, don't make copy just get reference

        @returns List of all children under this XMLTreeNode
        """
        return self._children

    def setData(self, data):
        """ Set node data, can be anything

        @param data Any data to set under this XMLTreeNode
        """
        self.tag = data

    def getData(self):
        """ Get the data under this XMLTreeNode

        @returns Data set under this XMLTreeNode
        """
        return self.tag

    def isData(self, name):
        """ Compare the data on this XMLTreeNode to name

        @param name The name to compare
        @returns True if name matches to the data, False otherwise
        """
        return (self.tag == name)

    def reparent(self, newparent, addchild=True):
        """ Reparent this XMLTreeNode under another XMLTreeNode

        @param newparent XMLTreeNode instance to become new parent of this XMLTreeNode
        @param addChild True if child needs to be added into parents list of children, False if not
        """
        if self.__parent == newparent:
            return

        # Need to make sure we're removed from possible old parent
        if self.__parent is not None:
            self.__parent.removeChild(self)

        # Set new parent
        self.__parent = newparent
        if addchild:
            self.__parent.addChild(self, reparent=False)

    def removeChild(self, child):
        """ Remove defined child from this XMLTreeNode's children list (if possible)

        @param child Instance of a XMLTreeNode
        @returns True on success, False otherwise (invalid child, child not under this XMLTreeNode)
        """
        if child.__parent != self:
            return False

        child.__parent = None

        # If out children does not have defined child this will fail,
        # that's why catching up ValueError and passing as nothing happened
        try:
            self._children.remove(child)
        except ValueError:
            return False

        return True

    def addAttrib(self, key, val):
        """ Add or overwrite attribute
        """
        self.attrib[key] = val

    def isAttrib(self, key):
        """ Checks if this node contains attribute
        @param key Attribute name
        @returns True if found, False otherwise
        """
        return (key in self.attrib)

    def getAttrib(self, key):
        """ Get attribute value by name
        @param key Attribute name
        @returns Attribute value or raises error
        """
        return self.attrib[key]

    def getAttribSafe(self, key):
        """ Get attribute value by name or None if not found
        @param key Attribute name
        @returns Attribute value or None
        """
        return self.attrib.get(key, None)

    def delAttrib(self, key):
        """ Remove attribute
        @param key Attribute name
        """
        del self.attrib[key]

    def getAttributes(self):
        """ Get all attributes as a dictionary
        @returns Dictionary containing all attributes
        """
        return self.attrib

    def getRoot(self):
        """ Get the root node
        @returns Root node instance or None if not found
        """
        root = self
        parent = root.getParent()
        while parent is not None:
            root = parent
            parent = root.getParent()

        return root

    def getParent(self):
        """ Return node parent

        @returns XMLTreeNode if this XMLTreeNode has a parent, None if this is the root node
        """
        return self.__parent

    def getSubTreeNodesByName(self, name):
        """ Get ALL nodes and their subtrees which contains certain named value as list of XMLTreeNodes.
        This allows future manipulation or queries to the tree. Also identifying each node's parent is easy with getParent()

        @param name Value to be search for
        @returns List of CustomXMLParser of the corresponding child trees

        @code
        For example:
        root = XMLTreeNode("root")
        a = XMLTreeNode("ChildA")
        b = XMLTreeNode("ChildB")
        c = XMLTreeNode("ChildC")
        root.addChild( a )
        root.addChild( b )
        root.addChild( c )
        a.addChild( XMLTreeNode("Test") )
        a.addChild( XMLTreeNode("Test2") )
        n = TreeNode("Test")
        b.addChild( n )
        n.addChild( XMLTreeNode("SubTest") )
        n.addChild( XMLTreeNode("SubTest2") )
        c.addChild( XMLTreeNode("Test") )
        c.addChild( XMLTreeNode("Other") )

        This would create tree like:

                         - Test
                       /
              -- ChildA--- Test2    - Subtest
            /                     /
        root ---- ChildB--- Test ----- SubTest2
            \
              -- ChildC -- Test
                       \
                         - Other
        @endcode

        Consider a call:
        root.getSubTreesByName("Test")
        It would return all XMLTreeNode named as "Test"

        As a note we just get exact matches, not partial matches
        We get only the named node and it's subtree, no parents or what so ever

        """
        trees = []
        for child in self._children:
            if child.isData(name):
                trees.append(child)
            if child._children:
                trees += child.getSubTreeNodesByName(name)
        return trees

    def getSelfAndSubTreeNodesByName(self, name):
        """ Check also if self/root matches for the name,
        after that take the subtree nodes

        @param name Value to be search for
        @returns List of CustomXMLParser of the corresponding child trees
        """
        trees = []
        if self.isData(name):
            trees.append(self)

        trees += self.getSubTreeNodesByName(name)
        return trees

    def getTreeNodeByName(self, name):
        """ This is like getSubTreeNodesByName but return just FIRST matching subtree

        @param name Value to be search for
        @returns Corresponding child tree item
        """
        if self.isData(name):
            return self

        for child in self._children:
            if child.isData(name):
                return child
            tmp = child.getTreeNodeByName(name)
            if tmp is not None:
                return tmp
        return None

    def __contains__(self, index):
        """ Checks if treenode contains some data

        @param index Key or data to check
        @returns True if data is found, False otherwise
        """
        if self.isData(index):
            return True
        if index in self._children:
            return True
        for child in self._children:
            if child.isData(index):
                return True

        if index in self.attrib:
            return True

        return False

    def __iter__(self):
        """ Iterates thorough the children

        @returns Iterator
        """
        # Generator way
        for child in self.getChildren():
            yield child

    class XMLTreeNodeList:
        """ List of tree nodes with special accessibility helpers
        """
        def __init__(self):
            """ Initialize XMLTreeNodeList
            """
            self.node_list = []

        def __solveData(self, instance):
            """ Solve the data from the XMLTreeNode
            @param instance Any XMLTreeNode instance
            @returns The instance or it's contents depending on the count of children, etc.
            """
            childs = instance._children
            if len(childs) == 1:
                return childs[0].getData()

            return instance

        def __getitem__(self, index):
            """ Get item from list by index or name

            @param index Index of the item or it's name
            @returns The item or None
            """
            if not self.node_list:
                return None
            ll = len(self.node_list)

            if type(index) == int:
                if index < ll:
                    return self.__solveData(self.node_list[index])
                return None

            for node in self.node_list:
                if index in node:
                    return self.__solveData(node)

            return None

        def __contains__(self, index):
            """ Check whether list contains certain named item

            @param index Name of the item
            @returns True if item found, False otherwise
            """
            for instance in self.node_list:
                if index in instance:
                    return True

            return False

        def __iter__(self):
            """ Returns iterator of the items

            @returns iterator of the items
            """
            return iter(self.node_list)

        def __len__(self):
            """ Get number of items

            @returns Number of items
            """
            return len(self.node_list)

        def append(self, var):
            """ Append item to node list

            @param var Item to be appended
            """
            self.node_list.append(var)

    def __getitem__(self, index):
        """ Get certain child by name

        @param index Name of the node
        @returns XMLTreeNode instance, it's data or None
        """
        res = []
        if self.isData(index):
            res = self._children
            if not res:
                return None
            ll = len(res)
            if ll == 1:
                cc = res[0]._children
                if len(cc) == 0:
                    return res[0].getData()

                res2 = self.XMLTreeNodeList()
                for res_data in res:
                    res2.append(res_data)
                return res2

            res2 = self.XMLTreeNodeList()
            for r in res:
                res2.append(r)
            return res2

        if list(self):
            res = self.XMLTreeNodeList()
            cc = self._children
            for c in cc:
                if c.isData(index):
                    res.append(c)

            ll = len(res)
            if ll == 1:
                return res
            elif ll == 0:
                return None
            else:
                return res

        if index in self.attrib:
            return self.attrib[index]
        return None

    def indent(self, elem, level=0):
        """ Fix indent of the elements, for pretty printing

        @param elem Element
        @param level Level of indent
        """
        i = '\n' + level * '  '
        if elem:
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def toSimpleString(self):
        """ Convert to XML string, does not do any formatting

        @returns XML presentation of the tree
        """
        res = element_tree.tostring(self)
        if sys.version >= '3':
            res = res.decode('utf-8', 'replace')
        return res

    def toString(self, doctype=''):
        """ Convert to XML string. Does formatting to a pretty presentation.
        Performance hit because copying the tree...

        @param doctype Documentation type added in the beginning of the return string
        @returns XML presentation of the tree
        """
        self.indent(self)
        res = element_tree.tostring(self)
        if sys.version >= '3':
            res = res.decode('utf-8', 'replace')

        return '%s%s' % (doctype, res)

    def toSortString(self):
        """ Get sortable string presentation

        @returns Sortable string presentation of this object
        """
        s = self.getData()
        if type(s) != str:
            return s

        sortedkeys = self.attrib.keys()
        sortedkeys = sorted(sortedkeys)
        arr = ""
        for key in sortedkeys:
            if arr:
                arr += ","
            arr += "'%s':'%s'" % (key, self.attrib[key])

        s += "{%s}" % (arr)
        s = s.replace(" ", "")
        return s

    def toRecursiveSortString(self):
        """ Get sortable string presentation of this and all children

        @returns Sortable string presentation of this object and it's children
        """
        s = "%s%s" % (self.getData(), self.attrib)
        data = self.getChildren()
        data = sorted(data, key=lambda k: k.toSortString())
        for i in data:
            s += i.toRecursiveSortString()
        s = s.replace(" ", "")
        return s

    def __str__(self):
        """ String presentation of this object

        @returns String presentation of this object
        """
        return self.toSimpleString()

    def __repr__(self):
        """ String presentation of this object

        @returns String presentation of this object
        """
        return "%x %s" % (id(self), "%s %s" % (("%s" % self.getData()).replace(" ", "").replace("'", ""), self.attrib))

# vi: tabstop=8 expandtab shiftwidth=4 softtabstop=4
