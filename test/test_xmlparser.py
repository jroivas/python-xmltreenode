import os
import unittest
import sys

if sys.version < '3':
    from StringIO import StringIO
else:
    from io import StringIO  # NOQA
try:
    import __builtin__
except ImportError:
    import builtins
    __builtin__ = builtins  # NOQA

# Make sure we'll find the required files...
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "xmltreenode"))
sys.path.append(os.path.dirname(__file__))

import xmlparser


def __outputDiff(string_a, string_b, index_a, pos):
    """ Outputs differences in two strings, used by assertEqualString.
    Raises ValueError

    @param string_a First string
    @param string_b Second string
    @param index_a Index in first string
    @param pos Position of difference
    """
    msg = "String difference at %s:\n" % (index_a)
    ba = (index_a - 20)
    if ba < 0:
        ba = 0
    aa = (index_a + 10)
    if aa > len(string_a):
        aa = len(string_a)
    ab = (index_a + 10)
    if ab > len(string_b):
        ab = len(string_b)

    msg_a = string_a[ba:aa]
    msg_b = string_b[ba:ab]
    pos += msg_a.count('\n')
    msg += "\n" + msg_a.replace('\n', '\\n') + "\n"
    msg += msg_b.replace('\n', '\\n') + "\n"
    if index_a < pos:
        pos = index_a
    msg += '-' * pos + '^'

    raise ValueError(msg)


def assertEqualString(string_a, string_b, ignoreSpace=False, ignoreNewLine=False):
    """ Asserts that given two strings are equal.
    Return silently when ok, otherwise raises exception with verbosal output.

    @param string_a First string
    @param string_b Secondb string
    @param ignoreSpace When comparing strings, ignore all space characters
    @param ignoreNewLine When comparing strings, ignore all new line characters
    """

    if string_a is None and string_b is None:
        return
    if string_a is None:
        raise ValueError('First string is None')
    if string_b is None:
        raise ValueError('Second string is None')

    index_a = 0
    if ignoreSpace:
        string_a = string_a.replace(' ', '')
        string_b = string_b.replace(' ', '')
    if ignoreNewLine:
        string_a = string_a.replace('\n', '')
        string_b = string_b.replace('\n', '')
    while index_a < len(string_a) and index_a < len(string_b):
        if string_a[index_a] != string_b[index_a]:
            __outputDiff(string_a, string_b, index_a, 20)
        index_a += 1
    if len(string_a) != len(string_b):
        pos = min(len(string_a), len(string_b))
        __outputDiff(string_a, string_b, index_a, pos)


class TestXmlparser(unittest.TestCase):
    def setUp(self):
        self.dummyXML = """
        <root>
            <a>
                <b></b>
            </a>
            <a myattr="c">
                <c />
                <c />
                <c2 />
            </a>
            <d>
                <e>1</e>
                <e>2</e>
                <e>3</e>
            </d>
        </root>
        """

    def test_xmlparser_CustomXMLParser_getRoot(self):
        iparse = xmlparser.CustomXMLParser()
        res = iparse.load(self.dummyXML, sourceIsFile=False)
        self.assertNotEqual(res, None)

        root = iparse.getRoot()
        self.assertEqual(root.getData(), "root")
        self.assertEqual(root.numChildren(), 3)

    def test_xmlparser_CustomXMLParser_getitem(self):
        iparse = xmlparser.CustomXMLParser()
        self.assertEqual(iparse["root"], None)
        res = iparse.load(self.dummyXML, sourceIsFile=False)
        self.assertNotEqual(res, None)

        root = iparse["root"]
        self.assertEqual(root["a"], "b")
        self.assertEqual(root["d"].numChildren(), 3)

    def test_xmlparser_CustomXMLParser_contains(self):
        iparse = xmlparser.CustomXMLParser()
        self.assertFalse("root" in iparse)

        res = iparse.load(self.dummyXML, sourceIsFile=False)
        self.assertNotEqual(res, None)

        self.assertTrue("root" in iparse)

    def test_xmlparser_start_and_end_basic(self):
        data = """<tag1>
  <tag2 a="1" b="2" c="3" d="4" />
  <tag3 attr1="1234567890" attr2="abcd1234" />
</tag1>
"""
        tag2_attr = {'b': '2', 'c': '3', 'd': '4', 'a': '1'}
        tag3_attr = {'attr1': '1234567890', 'attr2': 'abcd1234'}

        iparse = xmlparser.CustomXMLParser()

        iparse.start('tag1', None)
        iparse.end('tag1')
        iparse.start('tag2', tag2_attr)
        iparse.end('tag2')
        iparse.start('tag3', tag3_attr)
        iparse.end('tag3')

        assertEqualString(iparse.getRoot().toString(), data, ignoreSpace=True)

    def test_xmlparser_start_end_and_data_basic(self):
        data = """<tag1>
  <tag2 a="1" b="2" c="3" d="4">Hello!</tag2>
  <tag3 attr1="1234567890" attr2="abcd1234">Something important here.</tag3>
</tag1>
"""
        tag2_attr = {'b': '2', 'c': '3', 'd': '4', 'a': '1'}
        tag3_attr = {'attr1': '1234567890', 'attr2': 'abcd1234'}

        iparse = xmlparser.CustomXMLParser()

        iparse.start('tag1', None)
        iparse.end('tag1')
        iparse.start('tag2', tag2_attr)
        iparse.data("Hello!")
        iparse.end('tag2')
        iparse.start('tag3', tag3_attr)
        iparse.data("Something important here.")
        iparse.end('tag3')

        assertEqualString(iparse.getRoot().toString(), data, ignoreSpace=True)

    def test_xmlparser_load_singletag_xml(self):
        singletag = """<first>
  <tag name="%s" />
</first>
"""
        iparse = xmlparser.CustomXMLParser()
        res = iparse.load(singletag % 'tmp', sourceIsFile=False)

        self.assertNotEqual(type(res), list)
        self.assertEqual(len(res.getRoot()), 1)
        self.assertEqual(len(res), len(res.getRoot()))
        assertEqualString(res.getRoot().toString(), singletag % 'tmp', ignoreSpace=True)

    def test_xmlparser_load_singletag_xml_with_comment_lines(self):
        singletag = """<!-- THIS IS COMMENT -->
        <first>
        <tag name="tmp" />
        <!-- ANOTHER COMMENT
        WITH TWO LINES -->
        </first>
        """
        expected_output = """<first>
  <!-- THIS IS COMMENT -->
  <tag name="tmp" />
  <!-- ANOTHER COMMENT
        WITH TWO LINES -->
</first>
"""
        iparse = xmlparser.CustomXMLParser()
        res = iparse.load(singletag, sourceIsFile=False)

        assertEqualString(res.getRoot().toString(), expected_output, ignoreSpace=True)

    def test_xmlparser_load_multitag_xml_special_with_addDummy(self):
        tag1 = """<first>
  <tag args="tmp1" />
</first>
"""
        tag2 = """<second>
  <tag />
  <tag name="tmp2" />
</second>
"""
        multitag_special = tag1 + tag2
        multitag_special_with_dummy = """<dummy>
  <first>
    <tag args="tmp1" />
  </first>
  <second>
    <tag />
    <tag name="tmp2" />
  </second>
</dummy>
"""

        parse = xmlparser.CustomXMLParser()
        res = parse.load(multitag_special, sourceIsFile=False, addDummy=True)

        self.assertNotEqual(type(res), list)
        assertEqualString(res.getRoot().toString(), multitag_special_with_dummy, ignoreSpace=True)

        res = res.getRoot().getChildren()

        self.assertEqual(type(res), list)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].getData(), "first")
        self.assertEqual(res[1].getData(), "second")
        assertEqualString(res[0].toString(), tag1, ignoreSpace=True)
        assertEqualString(res[1].toString(), tag2, ignoreSpace=True)

    def test_xmlparser_load_invalid_xml_string_raise_IOError(self):
        singletag = """<first>
        <tag name="
        </first>
        """
        try:
            sys.stdout = StringIO()

            iparse = xmlparser.CustomXMLParser()

            self.assertRaisesRegexp(ValueError, 'Input is not valid XML: not well-formed', iparse.load, singletag, sourceIsFile=False)
        except:
            raise
        finally:
            sys.stdout = sys.__stdout__

    def _raise_exception(self, ex):
        raise ex

    def _dummy_return(self, value):
        return value

    def test_xmlparser_load_invalid_xml_file_raise_IOError(self):
        singletag = """<first>
        <tag name=
        </first>
        """
        iparse = xmlparser.CustomXMLParser()
        io = StringIO(singletag)
        try:
            orig_open = __builtin__.open
            __builtin__.open = lambda filen, mode: self._dummy_return(io)
            self.assertRaisesRegexp(ValueError, 'Input is not valid XML: dummy_file, not well-formed', iparse.load, 'dummy_file', sourceIsFile=True)
        except:
            raise
        finally:
            __builtin__.open = orig_open

    def test_xmlparser_load_invalid_file_raise_IOError(self):
        iparse = xmlparser.CustomXMLParser()
        try:
            orig_open = __builtin__.open
            __builtin__.open = lambda filen, mode: self._raise_exception(IOError("Error"))
            self.assertRaisesRegexp(ValueError, 'File dummy_file not found!', iparse.load, 'dummy_file', sourceIsFile=True)
        except:
            raise
        finally:
            __builtin__.open = orig_open

    def test_xmlparser_load_invalid_file_no_IOError_only_print(self):
        iparse = xmlparser.CustomXMLParser()
        try:
            sys.stdout = StringIO()
            orig_open = __builtin__.open
            __builtin__.open = lambda filen, mode: self._raise_exception(IOError("Error"))

            iparse.ignoreErrors(True)
            ret = iparse.load('dummy_file', sourceIsFile=True)

            self.assertEqual(ret, None)

            output = sys.stdout.getvalue().strip()

            self.assertEqual(output, "ERROR: File dummy_file not found!")
        except:
            raise
        finally:
            __builtin__.open = orig_open
            sys.stdout = sys.__stdout__

    def test_xmlparser_len_empty_zero(self):
        iparse = xmlparser.CustomXMLParser()

        self.assertEqual(len(iparse), 0)
