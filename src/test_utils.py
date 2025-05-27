import unittest

from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    text_node_to_html_node,
)


class TestTextToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_type_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)

    def test_text_type_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)

    def test_text_type_code(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
        self.assertEqual(html_node.props, None)

    def test_text_type_link(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_type_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text"}
        )


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_base_case(self):
        nodes = [TextNode("Hello **world**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
            ],
        )

    def test_multiple_inline_delimiters(self):
        nodes = [TextNode("This **is** a **test**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This ", TextType.TEXT),
                TextNode("is", TextType.BOLD),
                TextNode(" a ", TextType.TEXT),
                TextNode("test", TextType.BOLD),
            ],
        )

    def test_invalid_delimiter(self):
        nodes = [TextNode("Hello *world*", TextType.TEXT)]
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(str(context.exception), "wrong delimiter")

    def test_mismatched_delimiter_type(self):
        nodes = [TextNode("Hello **world**", TextType.TEXT)]
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(nodes, "**", TextType.ITALIC)
        self.assertIn(
            "Delimiter '**' does not match text type 'italic'", str(context.exception)
        )

    def test_unmatched_delimiter(self):
        nodes = [TextNode("Hello **world", TextType.TEXT)]
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "unmatching delimiter")

    def test_empty_text(self):
        nodes = [TextNode("", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_empty_parts(self):
        nodes = [TextNode("****", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_non_text_node_passthrough(self):
        nodes = [
            TextNode("This is plain", TextType.TEXT),
            TextNode("This is bold", TextType.BOLD),
            TextNode("This is italic", TextType.ITALIC),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is plain", TextType.TEXT),
                TextNode("This is bold", TextType.BOLD),
                TextNode("This is italic", TextType.ITALIC),
            ],
        )


class TestMarkdownExtractions(unittest.TestCase):
    def test_link_extraction(self):
        self.assertEqual(
            extract_markdown_links("[Google](https://google.com)"),
            [("Google", "https://google.com")],
        )
        self.assertEqual(
            extract_markdown_links("Visit [GitHub](https://github.com) today!"),
            [("GitHub", "https://github.com")],
        )

        self.assertEqual(
            extract_markdown_links("[A](a.com) and [B](b.com)"),
            [("A", "a.com"), ("B", "b.com")],
        )

    def test_extract_markdown_images(self):
        self.assertEqual(
            extract_markdown_images("![Python](python.png)"), [("Python", "python.png")]
        )
        self.assertEqual(
            extract_markdown_images("Here's an ![logo](logo.jpg) inside text."),
            [("logo", "logo.jpg")],
        )
        self.assertEqual(
            extract_markdown_images("![A](a.png) and ![B](b.png)"),
            [("A", "a.png"), ("B", "b.png")],
        )


if __name__ == "__main__":
    unittest.main()
