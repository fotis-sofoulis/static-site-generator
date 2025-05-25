import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
