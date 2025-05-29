import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
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


class TestSplitNodesImgLink(unittest.TestCase):
    def test_split_link_single(self):
        node = TextNode(
            "This is text with a [link](https://example.com) in it", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" in it", TextType.TEXT),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_edge_positions(self):
        node = TextNode("[start](start.com) middle [end](end.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("start", TextType.LINK, "start.com"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("end", TextType.LINK, "end.com"),
            ],
        )

    def test_non_text_node(self):
        node = TextNode("This shouldn't change", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_mixed_content(self):
        node = TextNode(
            "Text ![image](img.png) with [link](url.com) mixed", TextType.TEXT
        )
        # First split images
        image_nodes = split_nodes_image([node])
        # Then split links from those results
        link_nodes = split_nodes_link(image_nodes)
        self.assertEqual(
            link_nodes,
            [
                TextNode("Text ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img.png"),
                TextNode(" with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
                TextNode(" mixed", TextType.TEXT),
            ],
        )

    def test_split_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [])

    def test_split_image_empty_url(self):
        node = TextNode("Here's an ![image]() with empty URL", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Here's an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, ""),
                TextNode(" with empty URL", TextType.TEXT),
            ],
        )


class TestTextToTextNode(unittest.TestCase):
    def test_empty_text(self):
        self.assertEqual(text_to_textnodes(""), [])

    def test_mixed_markdown(self):
        nodes = text_to_textnodes(
            "This is **bold**, _italic_, `code`, ![image](url), and [link](url)"
        )
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(", ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(", and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
