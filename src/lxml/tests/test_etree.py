import unittest

from StringIO import StringIO
import os, shutil, tempfile
from lxml import c14n

class ETreeTestCaseBase(unittest.TestCase):
    etree = None
    
    def setUp(self):
        self._temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self._temp_dir)

    def getTestFilePath(self, name):
        return os.path.join(self._temp_dir, name)
    
    def test_element(self):
        for i in range(10):
            e = self.etree.Element('foo')

    def test_tree(self):
        Element = self.etree.Element
        ElementTree = self.etree.ElementTree
    
        element = Element('top')
        tree = ElementTree(element)
        self.buildNodes(element, 10, 3)
        f = open(self.getTestFilePath('testdump.xml'), 'w')
        tree.write(f, 'UTF-8')
        f.close()
        f = open(self.getTestFilePath('testdump.xml'), 'r')
        tree = ElementTree(file=f)
        f.close()
        f = open(self.getTestFilePath('testdump2.xml'), 'w')
        tree.write(f, 'UTF-8')
        f.close()
        f = open(self.getTestFilePath('testdump.xml'), 'r')
        data1 = f.read()
        f.close()
        f = open(self.getTestFilePath('testdump2.xml'), 'r')
        data2 = f.read()
        f.close()
        self.assertEquals(data1, data2)
        
    def buildNodes(self, element, children, depth):
        Element = self.etree.Element
        
        if depth == 0:
            return
        for i in range(children):
            new_element = Element('element_%s_%s' % (depth, i))
            self.buildNodes(new_element, children, depth - 1)
            element.append(new_element)

    def test_simple(self):
        Element = self.etree.Element
        
        root = Element('root')
        root.append(Element('one'))
        root.append(Element('two'))
        root.append(Element('three'))
        self.assertEquals(3, len(root))
        self.assertEquals('one', root[0].tag)
        self.assertEquals('two', root[1].tag)
        self.assertEquals('three', root[2].tag)
        self.assertRaises(IndexError, root.__getitem__, 3)

    def test_subelement(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement
        
        root = Element('root')
        SubElement(root, 'one')
        SubElement(root, 'two')
        SubElement(root, 'three')
        self.assertEquals(3, len(root))
        self.assertEquals('one', root[0].tag)
        self.assertEquals('two', root[1].tag)
        self.assertEquals('three', root[2].tag)
        
    def test_element_indexing_with_text(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc>Test<one>One</one></doc>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals(1, len(root))
        self.assertEquals('one', root[0].tag)
        self.assertRaises(IndexError, root.__getitem__, 1)
        
    def test_element_indexing_with_text2(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc><one>One</one><two>Two</two>hm<three>Three</three></doc>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals(3, len(root))
        self.assertEquals('one', root[0].tag)
        self.assertEquals('two', root[1].tag)
        self.assertEquals('three', root[2].tag)

    def test_element_indexing_only_text(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc>Test</doc>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals(0, len(root))

    def test_element_indexing_negative(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement
        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')
        d = SubElement(a, 'd')
        self.assertEquals(d, a[-1])
        self.assertEquals(c, a[-2])
        self.assertEquals(b, a[-3])
        self.assertRaises(IndexError, a.__getitem__, -4)
        a[-1] = e = Element('e')
        self.assertEquals(e, a[-1])
        del a[-1]
        self.assertEquals(2, len(a))
        
    def test_elementtree(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc><one>One</one><two>Two</two></doc>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals(2, len(root))
        self.assertEquals('one', root[0].tag)
        self.assertEquals('two', root[1].tag)

    def test_text(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc>This is a text</doc>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals('This is a text', root.text)

    def test_text_empty(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc></doc>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals(None, root.text)

    def test_text_other(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc><one>One</one></doc>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals(None, root.text)
        self.assertEquals('One', root[0].text)

    def test_tail(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc>This is <i>mixed</i> content.</doc>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals(1, len(root))
        self.assertEquals('This is ', root.text)
        self.assertEquals(None, root.tail)
        self.assertEquals('mixed', root[0].text)
        self.assertEquals(' content.', root[0].tail)

    def test_ElementTree(self):
        Element = self.etree.Element
        ElementTree = self.etree.ElementTree
        
        el = Element('hoi')
        doc = ElementTree(el)
        root = doc.getroot()
        self.assertEquals(None, root.text)
        self.assertEquals('hoi', root.tag)

    def test_attributes(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc one="One" two="Two"/>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals('One', root.attrib['one'])
        self.assertEquals('Two', root.attrib['two'])
        self.assertRaises(KeyError, root.attrib.__getitem__, 'three')  

    def test_attributes2(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc one="One" two="Two"/>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals('One', root.attrib.get('one'))
        self.assertEquals('Two', root.attrib.get('two'))
        self.assertEquals(None, root.attrib.get('three'))
        self.assertEquals('foo', root.attrib.get('three', 'foo'))

    def test_attributes3(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<doc one="One" two="Two"/>')
        doc = ElementTree(file=f)
        root = doc.getroot()
        self.assertEquals('One', root.get('one'))
        self.assertEquals('Two', root.get('two'))
        self.assertEquals(None, root.get('three'))
        self.assertEquals('foo', root.get('three', 'foo'))

    def test_attribute_keys(self):
        XML = self.etree.XML
        
        root = XML('<doc alpha="Alpha" beta="Beta" gamma="Gamma"/>')
        keys = root.attrib.keys()
        keys.sort()
        self.assertEquals(['alpha', 'beta', 'gamma'], keys)

    def test_attribute_keys2(self):
        XML = self.etree.XML
        
        root = XML('<doc alpha="Alpha" beta="Beta" gamma="Gamma"/>')
        keys = root.keys()
        keys.sort()
        self.assertEquals(['alpha', 'beta', 'gamma'], keys)

    def test_attribute_values(self):
        XML = self.etree.XML
        
        root = XML('<doc alpha="Alpha" beta="Beta" gamma="Gamma"/>')
        values = root.attrib.values()
        values.sort()
        self.assertEquals(['Alpha', 'Beta', 'Gamma'], values)

    def test_attribute_items(self):
        XML = self.etree.XML
        
        root = XML('<doc alpha="Alpha" beta="Beta" gamma="Gamma"/>')
        items = root.attrib.items()
        items.sort()
        self.assertEquals([
            ('alpha', 'Alpha'),
            ('beta', 'Beta'),
            ('gamma', 'Gamma'),
            ], 
            items)

    def test_XML(self):
        XML = self.etree.XML
        
        root = XML('<doc>This is a text.</doc>')
        self.assertEquals(0, len(root))
        self.assertEquals('This is a text.', root.text)

    def test_fromstring(self):
        fromstring = self.etree.fromstring

        root = fromstring('<doc>This is a text.</doc>')
        self.assertEquals(0, len(root))
        self.assertEquals('This is a text.', root.text)

    def test_iselement(self):
        iselement = self.etree.iselement
        Element = self.etree.Element
        ElementTree = self.etree.ElementTree
        XML = self.etree.XML
        Comment = self.etree.Comment
        
        el = Element('hoi')
        self.assert_(iselement(el))

        el2 = XML('<foo/>')
        self.assert_(iselement(el2))

        tree = ElementTree(element=Element('dag'))
        self.assert_(not iselement(tree))
        self.assert_(iselement(tree.getroot()))

        c = Comment('test')
        self.assert_(iselement(c))
        
    def test_iteration(self):
        XML = self.etree.XML
        
        root = XML('<doc><one/><two>Two</two>Hm<three/></doc>')
        result = []
        for el in root:
            result.append(el.tag)
        self.assertEquals(['one', 'two', 'three'], result)

    def test_iteration2(self):
        XML = self.etree.XML
        
        root = XML('<doc></doc>')
        result = []
        for el in root:
            result.append(el.tag)
        self.assertEquals([], result)

    def test_iteration3(self):
        XML = self.etree.XML
        
        root = XML('<doc>Text</doc>')
        result = []
        for el in root:
            result.append(el.tag)
        self.assertEquals([], result)
        
    def test_attribute_iterator(self):
        XML = self.etree.XML
        
        root = XML('<doc alpha="Alpha" beta="Beta" gamma="Gamma" />')
        result = []
        for key in root.attrib:
            result.append(key)
        result.sort()
        self.assertEquals(['alpha', 'beta', 'gamma'], result)

    def test_element_with_attributes(self):
        Element = self.etree.Element
        
        el = Element('tag', {'foo':'Foo', 'bar':'Bar'})
        self.assertEquals('Foo', el.attrib['foo'])
        self.assertEquals('Bar', el.attrib['bar'])

    def test_subelement_with_attributes(self):
        Element =  self.etree.Element
        SubElement = self.etree.SubElement
        
        el = Element('tag')
        SubElement(el, 'foo', baz="Baz")
        self.assertEquals("Baz", el[0].attrib['baz'])
        
    def test_write(self):
        ElementTree = self.etree.ElementTree
        XML = self.etree.XML

        for i in range(10):
            f = StringIO() 
            root = XML('<doc%s>This is a test.</doc%s>' % (i, i))
            tree = ElementTree(element=root)
            tree.write(f)
            data = f.getvalue()
            self.assertEquals(
                '<doc%s>This is a test.</doc%s>' % (i, i),
                c14n.canonicalize(data))

    # this could trigger a crash, apparently because the document
    # reference was prematurely garbage collected
    def test_crash(self):
        Element = self.etree.Element
        
        element = Element('tag')
        for i in range(10):
            element.attrib['key'] = 'value'
            value = element.attrib['key']
            self.assertEquals(value, 'value')
            
    # from doctest; for some reason this caused crashes too
    def test_write_ElementTreeDoctest(self):
        Element = self.etree.Element
        ElementTree = self.etree.ElementTree
        
        f = StringIO()
        for i in range(10):
            element = Element('tag%s' % i)
            self._check_element(element)
            tree = ElementTree(element)
            tree.write(f)
            self._check_element_tree(tree)

    def test_subelement_reference(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement
        
        el = Element('foo')
        el2 = SubElement(el, 'bar')
        el3 = SubElement(el2, 'baz')

        al = Element('foo2')
        al2 = SubElement(al, 'bar2')
        al3 = SubElement(al2, 'baz2')

        # now move al2 into el
        el.append(al2)

        # now change al3 directly
        al3.text = 'baz2-modified'

        # it should have changed through this route too
        self.assertEquals(
            'baz2-modified',
            el[1][0].text)

    def test_set_text(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement
        
        a = Element('a')
        b = SubElement(a, 'b')
        a.text = 'hoi'
        self.assertEquals(
            'hoi',
            a.text)
        self.assertEquals(
            'b',
            a[0].tag)

    def test_set_text2(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement
        
        a = Element('a')
        a.text = 'hoi'
        b = SubElement(a ,'b')
        self.assertEquals(
            'hoi',
            a.text)
        self.assertEquals(
            'b',
            a[0].tag)

    def test_set_text_none(self):
        Element = self.etree.Element

        a = Element('a')

        a.text = 'foo'
        a.text = None

        self.assertEquals(
            None,
            a.text)
        self.assertEquals(
            '<a></a>',
            self._writeElement(a))
        
    def test_tail1(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement
        
        a = Element('a')
        a.tail = 'dag'
        self.assertEquals('dag',
                          a.tail)
        b = SubElement(a, 'b')
        b.tail = 'hoi'
        self.assertEquals('hoi',
                          b.tail)

    def test_tail_append(self):
        Element = self.etree.Element
        
        a = Element('a')
        b = Element('b')
        b.tail = 'b_tail'
        a.append(b)
        self.assertEquals('b_tail',
                          b.tail)

    def test_tail_set_twice(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement
        
        a = Element('a')
        b = SubElement(a, 'b')
        b.tail = 'foo'
        b.tail = 'bar'
        self.assertEquals('bar',
                          b.tail)
        self.assertEquals(
            '<a><b></b>bar</a>',
            self._writeElement(a))

    def test_tail_set_none(self):
        Element = self.etree.Element
        a = Element('a')
        a.tail = 'foo'
        a.tail = None
        self.assertEquals(
            None,
            a.tail)
        self.assertEquals(
            '<a></a>',
            self._writeElement(a))
        
    def test_comment(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement
        Comment = self.etree.Comment

        a = Element('a')
        a.append(Comment('foo'))
        self.assertEquals(
            '<a><!-- foo --></a>',
            self._writeElement(a))

    def test_comment_whitespace(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement
        Comment = self.etree.Comment

        a = Element('a')
        a.append(Comment(' foo  '))
        self.assertEquals(
            '<a><!--  foo   --></a>',
            self._writeElement(a))  

    def test_comment_nonsense(self):
        Comment = self.etree.Comment
        c = Comment('foo')
        self.assertEquals({}, c.attrib)
        self.assertEquals([], c.keys())
        self.assertEquals([], c.items())
        self.assertEquals(None, c.get('hoi'))
        self.assertEquals(0, len(c))
        # should not iterate
        for i in c:
            pass

    def test_setitem(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = Element('c')
        a[0] = c
        self.assertEquals(
            c,
            a[0])
        self.assertEquals('<a><c></c></a>',
                          self._writeElement(a))
        self.assertEquals('<b></b>',
                          self._writeElement(b))

    def test_setitem2(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        for i in range(5):
            b = SubElement(a, 'b%s' % i)
            c = SubElement(b, 'c')
        for i in range(5):
            d = Element('d')
            e = SubElement(d, 'e')
            a[i] = d
        self.assertEquals(
            '<a><d><e></e></d><d><e></e></d><d><e></e></d><d><e></e></d><d><e></e></d></a>',
            self._writeElement(a))
        self.assertEquals('<c></c>',
                          self._writeElement(c))

    def test_setitem_indexerror(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')

        self.assertRaises(IndexError, a.__setitem__, 1, Element('c'))

    def test_tag_write(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')

        a.tag = 'c'

        self.assertEquals(
            'c',
            a.tag)

        self.assertEquals(
            '<c><b></b></c>',
            self._writeElement(a))

    def test_delitem(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')
        d = SubElement(a, 'd')

        del a[1]
        self.assertEquals(
            '<a><b></b><d></d></a>',
            self._writeElement(a))

        del a[0]
        self.assertEquals(
            '<a><d></d></a>',
            self._writeElement(a))

        del a[0]
        self.assertEquals(
            '<a></a>',
            self._writeElement(a))
        # move deleted element into other tree afterwards
        other = Element('other')
        other.append(c)
        self.assertEquals(
            '<other><c></c></other>',
            self._writeElement(other))

    def test_clear(self):
        Element = self.etree.Element
     
        a = Element('a')
        a.text = 'foo'
        a.tail = 'bar'
        a.set('hoi', 'dag')
        a.clear()
        self.assertEquals(None, a.text)
        self.assertEquals(None, a.tail)
        self.assertEquals(None, a.get('hoi'))
        self.assertEquals('a', a.tag)

    def test_clear_sub(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        a.text = 'foo'
        a.tail = 'bar'
        a.set('hoi', 'dag')
        b = SubElement(a, 'b')
        c = SubElement(b, 'c')
        a.clear()
        self.assertEquals(None, a.text)
        self.assertEquals(None, a.tail)
        self.assertEquals(None, a.get('hoi'))
        self.assertEquals('a', a.tag)
        self.assertEquals(0, len(a))
        self.assertEquals('<a></a>',
                          self._writeElement(a))
        self.assertEquals('<b><c></c></b>',
                          self._writeElement(b))

    def test_insert(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')
        d = Element('d')
        a.insert(0, d)

        self.assertEquals(
            d,
            a[0])

        self.assertEquals(
            '<a><d></d><b></b><c></c></a>',
            self._writeElement(a))

        e = Element('e')
        a.insert(2, e)
        self.assertEquals(
            e,
            a[2])
        self.assertEquals(
            '<a><d></d><b></b><e></e><c></c></a>',
            self._writeElement(a))

    def test_insert_beyond_index(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = Element('c')

        a.insert(2, c)
        self.assertEquals(
            c,
            a[1])
        self.assertEquals(
            '<a><b></b><c></c></a>',
            self._writeElement(a))

    def test_insert_negative(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')

        d = Element('d')
        a.insert(-1, d)
        self.assertEquals(
            d,
            a[-2])
        self.assertEquals(
            '<a><b></b><d></d><c></c></a>',
            self._writeElement(a))
        
    def test_remove(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')

        a.remove(b)
        self.assertEquals(
            c,
            a[0])
        self.assertEquals(
            '<a><c></c></a>',
            self._writeElement(a))

    def test_remove_nonexisting(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')
        d = Element('d')
        self.assertRaises(
            ValueError, a.remove, d)

    def test_getchildren(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')
        d = SubElement(b, 'd')
        e = SubElement(c, 'e')
        self.assertEquals(
            '<a><b><d></d></b><c><e></e></c></a>',
            self._writeElement(a))
        self.assertEquals(
            [b, c],
            a.getchildren())
        self.assertEquals(
            [d],
            b.getchildren())
        self.assertEquals(
            [],
            d.getchildren())

    def test_makeelement(self):
        Element = self.etree.Element

        a = Element('a')
        b = a.makeelement('c', {'hoi':'dag'})
        self.assertEquals(
            '<c hoi="dag"></c>',
            self._writeElement(b))

    def test_getiterator(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')
        d = SubElement(b, 'd')
        e = SubElement(c, 'e')

        self.assertEquals(
            [a, b, d, c, e],
            list(a.getiterator()))
        self.assertEquals(
            [d],
            list(d.getiterator()))

    def test_getiterator_filter(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')
        d = SubElement(b, 'd')
        e = SubElement(c, 'e')

        self.assertEquals(
            [a],
            list(a.getiterator('a')))
        a2 = SubElement(e, 'a')
        self.assertEquals(
            [a, a2],
            list(a.getiterator('a')))
        self.assertEquals(
            [a2],
            list(e.getiterator('a'))) 

    def test_getiterator_with_text(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        a.text = 'a'
        b = SubElement(a, 'b')
        b.text = 'b'
        b.tail = 'b1'
        c = SubElement(a, 'c')
        c.text = 'c'
        c.tail = 'c1'
        d = SubElement(b, 'd')
        c.text = 'd'
        c.tail = 'd1'
        e = SubElement(c, 'e')
        e.text = 'e'
        e.tail = 'e1'

        self.assertEquals(
            [a, b, d, c, e],
            list(a.getiterator()))
        #self.assertEquals(
        #    [d],
        #    list(d.getiterator()))

    def test_getiterator_filter_with_text(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        a.text = 'a'
        b = SubElement(a, 'b')
        b.text = 'b'
        b.tail = 'b1'
        c = SubElement(a, 'c')
        c.text = 'c'
        c.tail = 'c1'
        d = SubElement(b, 'd')
        c.text = 'd'
        c.tail = 'd1'
        e = SubElement(c, 'e')
        e.text = 'e'
        e.tail = 'e1'

        self.assertEquals(
            [a],
            list(a.getiterator('a')))
        a2 = SubElement(e, 'a')
        self.assertEquals(
            [a, a2],
            list(a.getiterator('a')))   
        self.assertEquals(
            [a2],
            list(e.getiterator('a')))

    def test_attribute_manipulation(self):
        Element = self.etree.Element

        a = Element('a')
        a.attrib['foo'] = 'Foo'
        a.attrib['bar'] = 'Bar'
        self.assertEquals('Foo', a.attrib['foo'])
        del a.attrib['foo']
        self.assertRaises(KeyError, a.attrib.__getitem__, 'foo')

    def test_getslice(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')
        d = SubElement(a, 'd')

        self.assertEquals(
            [b, c],
            a[0:2])
        self.assertEquals(
            [b, c, d],
            a[:])
        self.assertEquals(
            [b, c, d],
            a[:10])
        self.assertEquals(
            [b],
            a[0:1])
        self.assertEquals(
            [],
            a[10:12])

    def test_getslice_negative(self):
        Element = self.etree.Element
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        c = SubElement(a, 'c')
        d = SubElement(a, 'd')

        self.assertEquals(
            [d],
            a[-1:])
        self.assertEquals(
            [c, d],
            a[-2:])
        self.assertEquals(
            [c],
            a[-2:-1])
        self.assertEquals(
            [b, c],
            a[-3:-1])
        self.assertEquals(
            [b, c],
            a[-3:2])

    def test_getslice_text(self):
        ElementTree = self.etree.ElementTree
        
        f = StringIO('<a><b>B</b>B1<c>C</c>C1</a>')
        doc = ElementTree(file=f)
        a = doc.getroot()
        b = a[0]
        c = a[1]
        self.assertEquals(
            [b, c],
            a[:])
        self.assertEquals(
            [b],
            a[0:1])
        self.assertEquals(
            [c],
            a[1:])

    def test_comment_getitem_getslice(self):
        Element = self.etree.Element
        Comment = self.etree.Comment
        SubElement = self.etree.SubElement

        a = Element('a')
        b = SubElement(a, 'b')
        foo = Comment('foo')
        a.append(foo)
        c = SubElement(a, 'c')
        self.assertEquals(
            [b, foo, c],
            a[:])
        self.assertEquals(
            foo,
            a[1])
        a[1] = new = Element('new')
        self.assertEquals(
            new,
            a[1])
        self.assertEquals(
            '<a><b></b><new></new><c></c></a>',
            self._writeElement(a))
            
##     def test_setslice(self):
##         Element = self.etree.Element
##         SubElement = self.etree.SubElement

##         a = Element('a')
##         b = SubElement(a, 'b')
##         c = SubElement(a, 'c')
##         d = SubElement(a, 'd')

##         e = Element('e')
##         f = Element('f')
##         g = Element('g')

##         s = [e, f, g]
##         a[1:2] = s
##         self.assertEquals(
##             [b, e, f, g, d],
##             list(a))
        
# TypeError in etree, AssertionError in ElementTree; difference deemed to be acceptable for now
##     def test_setitem_assert(self):
##         Element = self.etree.Element
##         SubElement = self.etree.SubElement

##         a = Element('a')
##         b = SubElement(a, 'b')
        
##         self.assertRaises(AssertionError,
##                           a.__setitem__, 0, 'foo')
        
# gives error in ElementTree
##     def test_comment_empty(self):
##         Element = self.etree.Element
##         Comment = self.etree.Comment

##         a = Element('a')
##         a.append(Comment())
##         print self._writeElement(a)
##         self.assertEquals(
##             '<a><!----></a>',
##             self._writeElement(a))

    def _writeElement(self, element):
        """Write out element for comparison.
        """
        ElementTree = self.etree.ElementTree
        f = StringIO()
        tree = ElementTree(element=element)
        tree.write(f)
        data = f.getvalue()
        return c14n.canonicalize(data)
                           
    def _check_element_tree(self, tree):
        self._check_element(tree.getroot())
        
    def _check_element(self, element):
        self.assert_(hasattr(element, 'tag'))
        self.assert_(hasattr(element, 'attrib'))
        self.assert_(hasattr(element, 'text'))
        self.assert_(hasattr(element, 'tail'))
        self._check_string(element.tag)
        self._check_mapping(element.attrib)
        if element.text != None:
            self._check_string(element.text)
        if element.tail != None:
            self._check_string(element.tail)
        
    def _check_string(self, string):
        len(string)
        for char in string:
            self.assertEquals(1, len(char))
        new_string = string + ""
        new_string = string + " "
        string[:0]

    def _check_mapping(self, mapping):
        len(mapping)
        keys = mapping.keys()
        items = mapping.items()
        for key in keys:
            item = mapping[key]
        mapping["key"] = "value"
        self.assertEquals("value", mapping["key"])

from lxml import etree

class ETreeTestCase(ETreeTestCaseBase):
    etree = etree

try:
    from elementtree import ElementTree
    HAVE_ELEMENTTREE = 1
except ImportError:
    HAVE_ELEMENTTREE = 0

if HAVE_ELEMENTTREE:
    class ElementTreeTestCase(ETreeTestCaseBase):
        etree = ElementTree
    
def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([unittest.makeSuite(ETreeTestCase)])
    if HAVE_ELEMENTTREE:
        suite.addTests([unittest.makeSuite(ElementTreeTestCase)])
    return suite

if __name__ == '__main__':
    unittest.main()
