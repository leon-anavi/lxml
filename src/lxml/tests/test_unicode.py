# -*- coding: utf-8 -*-
import unittest, doctest, sys, os.path

this_dir = os.path.dirname(__file__)
if this_dir not in sys.path:
    sys.path.insert(0, this_dir) # needed for Py3

from common_imports import StringIO, etree, SillyFileLike, HelperTestCase
from common_imports import _str, _bytes

try:
    unicode
except NameError:
    unicode = str

ascii_uni = _bytes('a').decode('utf8')

klingon = _bytes("\\uF8D2").decode("unicode_escape") # not valid for XML names

invalid_tag = _bytes("test").decode('utf8') + klingon

uni = _bytes('\\xc3\\u0680\\u3120').decode("unicode_escape") # some non-ASCII characters

uxml = _bytes("<test><title>test \\xc3\\xa1\\u3120</title><h1>page \\xc3\\xa1\\u3120 title</h1></test>"
              ).decode("unicode_escape")

class UnicodeTestCase(HelperTestCase):
    def test_unicode_xml(self):
        tree = etree.XML('<p>%s</p>' % uni)
        self.assertEqual(uni, tree.text)

    def test_unicode_xml_broken(self):
        uxml = ('<?xml version="1.0" encoding="UTF-8"?>' +
                '<p>%s</p>' % uni)
        self.assertRaises(ValueError, etree.XML, uxml)

    def test_unicode_tag(self):
        el = etree.Element(uni)
        self.assertEqual(uni, el.tag)

    def test_unicode_tag_invalid(self):
        # sadly, Klingon is not well-formed
        self.assertRaises(ValueError, etree.Element, invalid_tag)

    def test_unicode_nstag(self):
        tag = "{http://abc/}%s" % uni
        el = etree.Element(tag)
        self.assertEqual(tag, el.tag)

    def test_unicode_ns_invalid(self):
        # namespace URIs must conform to RFC 3986
        tag = "{http://%s/}abc" % uni
        self.assertRaises(ValueError, etree.Element, tag)

    def test_unicode_nstag_invalid(self):
        # sadly, Klingon is not well-formed
        tag = "{http://abc/}%s" % invalid_tag
        self.assertRaises(ValueError, etree.Element, tag)

    def test_unicode_qname(self):
        qname = etree.QName(uni, uni)
        tag = "{%s}%s" % (uni, uni)
        self.assertEqual(qname.text, tag)
        self.assertEqual(unicode(qname), tag)

    def test_unicode_qname_invalid(self):
        self.assertRaises(ValueError, etree.QName, invalid_tag)

    def test_unicode_attr(self):
        el = etree.Element('foo', {'bar': uni})
        self.assertEqual(uni, el.attrib['bar'])

    def test_unicode_comment(self):
        el = etree.Comment(uni)
        self.assertEqual(uni, el.text)

    def test_unicode_parse_stringio(self):
        el = etree.parse(StringIO('<p>%s</p>' % uni)).getroot()
        self.assertEqual(uni, el.text)

##     def test_parse_fileobject_unicode(self):
##         # parse unicode from unamed file object (not support by ElementTree)
##         f = SillyFileLike(uxml)
##         root = etree.parse(f).getroot()
##         self.assertEqual(unicode(etree.tostring(root, 'UTF-8'), 'UTF-8'),
##                           uxml)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([unittest.makeSuite(UnicodeTestCase)])
    return suite
