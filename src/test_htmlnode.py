import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_repr(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("<a>", "test", "", props)

        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")

    def test_empty(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_not_impl(self):
        node = HTMLNode("<a>", "test", "", "")

        self.assertRaises(NotImplementedError, node.to_html)


class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello world")
        self.assertEqual(node.to_html(), "Hello world")

    def test_to_html_with_tag(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click me</a>')

    def test_to_html_missing_value(self):
        node = LeafNode("span", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "no given value")


class TestParentNode(unittest.TestCase):
    def test_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_none_child(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", None).to_html()
        self.assertEqual(str(context.exception), "no children given")

    def test_empty_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", []).to_html()
        self.assertEqual(str(context.exception), "empty children list")

    def test_mixed_children_types(self):
        node = ParentNode("div", [
            LeafNode(None, "Raw text"),
            ParentNode("p", [LeafNode(None, "Paragraph text")]),
            LeafNode("a", "WOW!", {"href": "this is definetely a link", "target": "_blank"})
        ])
        expected = '<div>Raw text<p>Paragraph text</p><a href=\"this is definetely a link\" target=\"_blank\">WOW!</a></div>'
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
