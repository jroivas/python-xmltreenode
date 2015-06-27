import os
import unittest
import sys

# Make sure we'll find the required files...
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "xmltreenode"))
sys.path.append(os.path.dirname(__file__))

import xmltreenode


class TestTreenode(unittest.TestCase):
    def setUp(self):
        self.node = xmltreenode.XMLTreeNode("root")
        self.c1 = xmltreenode.XMLTreeNode("child1")
        self.c2 = xmltreenode.XMLTreeNode("child2")
        self.c3 = xmltreenode.XMLTreeNode("child3")
        self.node.addChild(self.c1)
        self.node.addChild(self.c2)
        self.c2.addChild(self.c3)

        self.root = xmltreenode.XMLTreeNode("root")
        self.a = xmltreenode.XMLTreeNode("ChildA")
        self.b = xmltreenode.XMLTreeNode("ChildB")
        self.c = xmltreenode.XMLTreeNode("ChildC")
        self.root.addChild(self.a)
        self.root.addChild(self.b)
        self.root.addChild(self.c)
        self.aa = xmltreenode.XMLTreeNode("Test")
        self.ab = xmltreenode.XMLTreeNode("Test2")
        self.a.addChild(self.aa)
        self.a.addChild(self.ab)
        self.ba = xmltreenode.XMLTreeNode("Test")
        self.b.addChild(self.ba)
        self.baa = xmltreenode.XMLTreeNode("SubTest")
        self.bab = xmltreenode.XMLTreeNode("SubTest2")
        self.ba.addChild(self.baa)
        self.ba.addChild(self.bab)
        self.ca = xmltreenode.XMLTreeNode("Test")
        self.cb = xmltreenode.XMLTreeNode("Other")
        self.cc = xmltreenode.XMLTreeNode("Test2")
        self.c.addChild(self.ca)
        self.c.addChild(self.cb)
        self.c.addChild(self.cc)

        self.iters = xmltreenode.XMLTreeNode("root")
        self.iters.addChild(xmltreenode.XMLTreeNode("Test"))
        self.iters.addChild(xmltreenode.XMLTreeNode("Test"))
        self.iters.addChild(xmltreenode.XMLTreeNode("Test2"))
        self.iters_o = xmltreenode.XMLTreeNode("Other")
        self.iters_o.addChild(xmltreenode.XMLTreeNode("Test"))
        self.iters.addChild(self.iters_o)

    def test_treeNode(self):
        node = self.node
        c1 = self.c1
        c2 = self.c2
        c3 = self.c3
        node.addAttrib("root", "value")
        self.assertEqual(node.getAttrib("root"), "value")
        node.addAttrib("tag", "test")
        self.assertEqual(node.getAttrib("tag"), "test")

        self.assertEqual(c1.getParent(), node)
        self.assertEqual(c2.getParent(), node)
        self.assertEqual(c3.getParent(), c2)
        self.assertEqual(node.getParent(), None)

        self.assertEqual(node.numChildren(), 2)

    def test_xmltreenode_deepcopy(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        node.addChild(child_a)
        node.addChild(xmltreenode.XMLTreeNode("b"))

        deepcopynode = node.deepcopy()
        self.assertNotEqual(id(node), id(deepcopynode))
        self.assertEqual(len(node), node.numChildren())
        self.assertEqual(len(node), len(deepcopynode))

        node_child = node.getChildren()
        deepcopynode_child = deepcopynode.getChildren()
        # Deepcopy copies children as well
        for i in range(len(node)):
            self.assertNotEqual(node_child[i], deepcopynode_child[i])

    def test_xmltreenode_copy(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        node.addChild(child_a)
        node.addChild(xmltreenode.XMLTreeNode("b"))
        copynode = node.copy()

        self.assertNotEqual(id(node), id(copynode))
        self.assertEqual(len(node), node.numChildren())
        self.assertEqual(len(node), len(copynode))

        node_child = node.getChildren()
        copynode_child = copynode.getChildren()
        # In case of copy we still have same children
        for i in range(len(node)):
            self.assertEqual(node_child[i], copynode_child[i])

    def test_treeNode_setValue_getValue_and_appendValue(self):
        node = xmltreenode.XMLTreeNode("root")
        self.assertEqual(node.getValue(), "")

        node.setValue("TEST")
        self.assertEqual(node.getValue(), "TEST")

        node.appendValue("_SOMETHING")
        self.assertEqual(node.getValue(), "TEST_SOMETHING")

    def test_treeNode_reparent(self):
        node = self.node
        c1 = self.c1
        c2 = self.c2
        c3 = self.c3

        c2.reparent(c1)
        self.assertEqual(c1.getParent(), node)
        self.assertEqual(c2.getParent(), c1)
        self.assertEqual(c3.getParent(), c2)

        self.assertEqual(node.numChildren(), 1)

        c2.reparent(node)
        self.assertEqual(c2.getParent(), node)
        self.assertEqual(node.numChildren(), 2)

    def test_treeNode_removeChild(self):
        node = self.node
        c1 = self.c1

        self.assertTrue(node.removeChild(c1))
        self.assertFalse(node.removeChild(c1))
        self.assertEqual(c1.getParent(), None)

        self.assertEqual(node.numChildren(), 1)

        node.addChild(c1)

    def test_xmltreenode_insertAfterChild(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        node.addChild(child_a)
        node.addChild(child_b)

        child_c = xmltreenode.XMLTreeNode("c")

        self.assertEqual(len(node), 2)

        node.insertAfterChild(child_a, child_c)
        self.assertEqual(len(node), 3)

        # Check have same output
        node_child = node.getChildrenRef()
        self.assertEqual(node_child[0], child_a)
        self.assertEqual(node_child[1], child_c)
        self.assertEqual(node_child[2], child_b)
        self.assertEqual(node_child[0].getRoot(), node_child[1].getRoot())

    def test_xmltreenode_insertAfterChild_without_reparenting(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        node.addChild(child_a)
        node.addChild(child_b)

        child_c = xmltreenode.XMLTreeNode("c")

        self.assertEqual(len(node), 2)

        node.insertAfterChild(child_a, child_c, reparent=False)
        self.assertEqual(len(node), 3)

        # Check have same output
        node_child = node.getChildrenRef()
        self.assertEqual(node_child[0], child_a)
        self.assertEqual(node_child[1], child_c)
        self.assertEqual(node_child[2], child_b)

    def test_xmltreenode_insertAfterChild_after_child_not_found_append_added_child_to_list(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        node.addChild(child_a)
        node.addChild(child_b)

        child_c = xmltreenode.XMLTreeNode("c")
        child_d = xmltreenode.XMLTreeNode("d")

        self.assertEqual(len(node), 2)

        node.insertAfterChild(child_c, child_d)
        self.assertEqual(len(node), 3)

        # Check have same output
        node_child = node.getChildrenRef()
        self.assertEqual(node_child[0], child_a)
        self.assertEqual(node_child[1], child_b)
        self.assertEqual(node_child[2], child_d)

    def test_xmltreenode_insertAfterChild_multiple_childrens(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        node.addChild(child_a)
        node.addChild(child_b)

        child_c = xmltreenode.XMLTreeNode("c")
        child_d = xmltreenode.XMLTreeNode("d")

        self.assertEqual(len(node), 2)

        node.insertAfterChild(child_a, child_d)
        self.assertEqual(len(node), 3)
        node.insertAfterChild(child_a, child_c)
        self.assertEqual(len(node), 4)

        # Check have same output
        node_child = node.getChildrenRef()
        self.assertEqual(node_child[0], child_a)
        self.assertEqual(node_child[1], child_c)
        self.assertEqual(node_child[2], child_d)
        self.assertEqual(node_child[3], child_b)

    def test_xmltreenode_insertChild(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        node.addChild(child_a)
        node.addChild(child_b)

        child_c = xmltreenode.XMLTreeNode("c")

        self.assertEqual(len(node), 2)

        node.insertChild(0, child_c)
        self.assertEqual(len(node), 3)

        # Check have same output
        node_child = node.getChildrenRef()
        self.assertEqual(node_child[0], child_c)
        self.assertEqual(node_child[1], child_a)
        self.assertEqual(node_child[2], child_b)
        self.assertEqual(node_child[0].getRoot(), node_child[1].getRoot())

    def test_xmltreenode_insertChild_without_reparenting(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        node.addChild(child_a)
        node.addChild(child_b)

        child_c = xmltreenode.XMLTreeNode("c")

        self.assertEqual(len(node), 2)

        node.insertChild(1, child_c, reparent=False)
        self.assertEqual(len(node), 3)

        # Check have same output
        node_child = node.getChildrenRef()
        self.assertEqual(node_child[0], child_a)
        self.assertEqual(node_child[1], child_c)
        self.assertEqual(node_child[2], child_b)
        self.assertNotEqual(node_child[0].getRoot(), node_child[1].getRoot())

    def test_xmltreenode_insertChild_multiple_childs(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        node.addChild(child_a)
        node.addChild(child_b)

        child_c = xmltreenode.XMLTreeNode("c")
        child_d = xmltreenode.XMLTreeNode("d")

        self.assertEqual(len(node), 2)

        node.insertChild(0, child_c)
        self.assertEqual(len(node), 3)
        node.insertChild(2, child_d)
        self.assertEqual(len(node), 4)

        # Check have same output
        node_child = node.getChildrenRef()
        self.assertEqual(node_child[0], child_c)
        self.assertEqual(node_child[1], child_a)
        self.assertEqual(node_child[2], child_d)
        self.assertEqual(node_child[3], child_b)

    def test_xmltreenode_append_insert_and_remove(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        child_c = xmltreenode.XMLTreeNode("c")

        self.assertEqual(node.getChildren(), [])

        node.append(child_a)

        self.assertEqual(node.getChildren(), [child_a])

        node.insert(0, child_b)
        node.insert(2, child_c)

        self.assertEqual(node.getChildren(), [child_b, child_a, child_c])

        node.remove(child_a)

        self.assertEqual(node.getChildren(), [child_b, child_c])

    def test_xmltreenode_numChildren(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        node.addChild(child_a)
        node.addChild(child_b)

        child_c = xmltreenode.XMLTreeNode("c")

        self.assertEqual(node.numChildren(), 2)

        node.addChild(child_c)
        self.assertEqual(node.numChildren(), 3)

    def test_xmltreenode_getChildren_and_getChildrenRef(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        child_c = xmltreenode.XMLTreeNode("c")
        node.addChild(child_a)
        node.addChild(child_b)

        childs = node.getChildren()
        childs_ref = node.getChildrenRef()
        self.assertListEqual(childs, childs_ref)
        self.assertNotEqual(id(childs), id(childs_ref))

        node.addChild(child_c)

        childs_new = node.getChildren()
        childs_ref_new = node.getChildrenRef()
        self.assertListEqual(childs_new, childs_ref_new)
        self.assertNotEqual(id(childs_new), id(childs_ref_new))

        self.assertEqual(id(childs_ref), id(childs_ref_new))
        self.assertNotEqual(id(childs), id(childs_new))

    def test_xmltreenode_setData_and_getData(self):
        root = "root"
        node = xmltreenode.XMLTreeNode(root)
        test_data = "test_data"

        self.assertEqual(node.getData(), root)
        node.setData(test_data)
        self.assertEqual(node.getData(), test_data)

        self.assertTrue(node.isData(test_data))
        self.assertFalse(node.isData("random"))

    def test_xmltreenode_reparent(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")

        orig_root = node.getRoot()
        node.reparent(child_a)
        new_root = node.getRoot()
        self.assertNotEqual(orig_root, new_root)
        self.assertEqual(new_root.toSimpleString(), '<a><root /></a>')

    def test_xmltreenode_reparent_child_not_added(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")

        orig_root = node.getRoot()
        node.reparent(child_a, addchild=False)
        new_root = node.getRoot()
        self.assertNotEqual(orig_root, new_root)
        self.assertEqual(new_root.toSimpleString(), '<a />')

    def test_xmltreenode_reparent_parent(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")

        orig_root = node.getRoot()
        node.reparent(child_a)
        new_root = node.getRoot()
        self.assertNotEqual(orig_root, new_root)
        self.assertEqual(new_root.toSimpleString(), '<a><root /></a>')
        node.reparent(child_a)
        new_root_2 = node.getRoot()
        self.assertEqual(new_root, new_root_2)
        self.assertEqual(new_root_2.toSimpleString(), '<a><root /></a>')

    def test_xmltreenode_removeChild(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        node.addChild(child_a)
        node.addChild(child_b)

        self.assertEqual(len(node), 2)
        self.assertTrue(node.removeChild(child_a))

        node_child = node.getChildrenRef()
        self.assertEqual(len(node), 1)
        self.assertEqual(node_child[0], child_b)

    def test_xmltreenode_removeChild_child_not_in_parents_child_list(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_a.reparent(node, addchild=False)

        self.assertFalse(node.removeChild(child_a))

    def test_xmltreenode_removeChild_removed_child_has_different_parent(self):
        node = xmltreenode.XMLTreeNode("root")
        node2 = xmltreenode.XMLTreeNode("root2")
        child_a = xmltreenode.XMLTreeNode("a")
        child_b = xmltreenode.XMLTreeNode("b")
        child_c = xmltreenode.XMLTreeNode("c")
        node.addChild(child_a)
        node.addChild(child_b)
        node.addChild(child_c)
        node2.addChild(child_c)

        self.assertFalse(node.removeChild(node2.getChildrenRef()[0]))

    def test_treeNode_attributes(self):
        node = self.node
        self.assertEqual(node.getAttributes(), {})

        # test addAttrib and getAttrib
        node.addAttrib("root", "value")
        self.assertEqual(node.getAttrib("root"), "value")

        node.addAttrib("tag", "test")
        self.assertEqual(node.getAttrib("tag"), "test")

        # Test isAttrib
        self.assertTrue(node.isAttrib("tag"))
        self.assertFalse(node.isAttrib("tag22"))

        # Test getAttribSafe
        self.assertEqual(node.getAttribSafe("root"), "value")
        self.assertEqual(node.getAttribSafe("None"), None)

        # Test getAttributes
        self.assertDictEqual(node.getAttributes(), {"root": "value", "tag": "test"})

        # Test delAttrib
        node.delAttrib('tag')
        self.assertFalse(node.isAttrib("tag"))
        self.assertDictEqual(node.getAttributes(), {"root": "value"})

    def test_xmltreenode_getRoot(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        node.addChild(child_a)

        self.assertEqual(node.getRoot().toSimpleString(), child_a.getRoot().toSimpleString())
        self.assertEqual(node.getRoot().toSimpleString(), "<root><a /></root>")

    def test_xmltreenode_getParent(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        node.addChild(child_a)

        self.assertEqual(child_a.getParent(), node)

    def test_xmltreenode_getSubTreeNodesByName(self):
        root = self.root

        ret_tree = root.getSubTreeNodesByName('Test')
        self.assertEqual(len(ret_tree), 3)
        self.assertIn(self.aa, ret_tree)
        self.assertIn(self.ba, ret_tree)
        self.assertIn(self.ca, ret_tree)

    def test_xmltreenode_getTreeNodeByName(self):
        root = self.root

        ret_val = root.getTreeNodeByName('Test')
        self.assertEqual(ret_val, self.aa)

        ret_val = root.getTreeNodeByName('SubTest2')
        self.assertEqual(ret_val, self.bab)

    def test_xmltreenode_getTreeNodeByName_name_not_found(self):
        root = self.root

        ret_val = root.getTreeNodeByName('NotFound')
        self.assertEqual(ret_val, None)

    def test_xmltreenode_getTreeNodeByName_name_root(self):
        root = self.root

        ret_val = root.getTreeNodeByName('root')
        self.assertEqual(ret_val, self.root)

    def test_xmltreenode_XMLTreeNodeList(self):
        tree_node_list = xmltreenode.XMLTreeNode.XMLTreeNodeList()
        child_a = xmltreenode.XMLTreeNode("a")

        self.assertEqual(len(tree_node_list), 0)

        tree_node_list.append(self.root)
        tree_node_list.append(self.a)
        tree_node_list.append(self.b)

        self.assertEqual(len(tree_node_list), 3)

        self.assertIn(self.a, tree_node_list)
        self.assertNotIn(child_a, tree_node_list)

        self.assertEqual(tree_node_list[0], self.root)
        self.assertEqual(tree_node_list[10], None)

    def test_xmltreenode_indent_and_toString(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_aa = xmltreenode.XMLTreeNode("aa")
        child_a.addChild(child_aa)
        node.addChild(child_a)
        expected_output = "<root>\n  <a>\n    <aa />\n  </a>\n</root>\n"

        node.indent(child_a)

        self.assertEqual(node.toString(), expected_output)

    def test_xmltreenode_toString(self):
        node = xmltreenode.XMLTreeNode("root")
        child_a = xmltreenode.XMLTreeNode("a")
        child_aa = xmltreenode.XMLTreeNode("aa")
        child_aaa = xmltreenode.XMLTreeNode("aaa")
        child_aa.addChild(child_aaa)
        child_a.addChild(child_aa)
        node.addChild(child_a)
        expected_output = "<root>\n  <a>\n    <aa>\n      <aaa />\n    </aa>\n  </a>\n</root>\n"

        self.assertEqual(node.toString(), expected_output)

    def test_xmltreenode_toSortString(self):
        node = xmltreenode.XMLTreeNode("root")
        node.addAttrib("root", "value")
        node.addAttrib("a", "test")
        expected_output = "root{'a':'test','root':'value'}"

        self.assertEqual(node.toSortString(), expected_output)

    def test_xmltreenode_toRecursiveSortString(self):
        node = xmltreenode.XMLTreeNode("root")
        node.addAttrib("root", "value")
        child_a = xmltreenode.XMLTreeNode("a")
        child_a.addAttrib("a", "test")
        node.addChild(child_a)
        expected_output = "root{'root':'value'}a{'a':'test'}"

        self.assertEqual(node.toRecursiveSortString(), expected_output)

    def test_xmltreenode_finditer(self):
        node = self.iters
        index = 0
        for elem in node.finditer("Test"):
            self.assertEqual(elem.getData(), "Test")
            index += 1
        self.assertEqual(index, 2)

    def test_xmltreenode_findall(self):
        node = self.iters
        self.assertEqual(len(node.findall("Test")), 2)
        self.assertEqual(len(node.findall("not_existing_child")), 0)

    def test_xmltreenode_iter_start(self):
        node = self.iters
        index = 0
        for elem in node.iter('*'):
            index += 1
        self.assertEqual(index, 6)

    def test_xmltreenode_iter(self):
        node = self.iters
        index = 0
        for elem in node.iter():
            index += 1
        self.assertEqual(index, 6)

    def test_xmltreenode_iter_element(self):
        node = self.iters
        index = 0
        for elem in node.iter('Test'):
            index += 1
        self.assertEqual(index, 3)

    def test_xmltreenode_getSelfAndSubTreeNodesByName(self):
        node = self.iters
        items = node.getSelfAndSubTreeNodesByName('Test')
        self.assertEqual(len(items), 3)

        items = node.getSelfAndSubTreeNodesByName('root')
        self.assertEqual(len(items), 1)
