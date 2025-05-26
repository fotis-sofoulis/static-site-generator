import unittest

from htmlnode import HTMLNode, LeafNode


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
        self.assertEqual(node.to_html(), "\"Hello world\"")

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


if __name__ == "__main__":
    unittest.main()
