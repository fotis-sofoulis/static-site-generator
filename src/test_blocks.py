import unittest

from blocks import (
    BlockType,
    block_to_block_type,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_edge_cases(self):
        self.assertEqual(markdown_to_blocks(""), [])

        self.assertEqual(markdown_to_blocks("   \n\n  \n"), [])

        md = "   \n\nSingle block\n\n   "
        self.assertEqual(markdown_to_blocks(md), ["Single block"])

    def test_consecutive_empty_lines(self):
        md = """
First block


Second block after multiple newlines


Third block


"""
        expected = [
            "First block",
            "Second block after multiple newlines",
            "Third block",
        ]
        self.assertEqual(markdown_to_blocks(md), expected)


class TestBlockToBlockType(unittest.TestCase):
    def test_empty_block(self):
        self.assertIsNone(block_to_block_type(""))

    def test_heading_blocks(self):
        for i in range(1, 7):
            block = "#" * i + " This is a heading"
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        self.assertNotEqual(block_to_block_type("##Not a heading"), BlockType.HEADING)

    def test_code_block(self):
        block = "```code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = """```
        multi-line
        code block
        ```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        self.assertNotEqual(block_to_block_type("```not closed"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("not opened```"), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        multiline_block = """> Line one
> Line two
> Line three"""
        self.assertEqual(block_to_block_type(multiline_block), BlockType.QUOTE)

        error_block = """> Line one
Not a quote
> Line three"""
        self.assertNotEqual(block_to_block_type(error_block), BlockType.QUOTE)

    def test_unordered_list_block(self):
        block = "- Item one"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        multiline_block = """- Item one
- Item two
- Item three"""
        self.assertEqual(block_to_block_type(multiline_block), BlockType.UNORDERED_LIST)

        error_block = """- Item one
Not a list item
- Item three"""
        self.assertNotEqual(block_to_block_type(error_block), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        block = "1. Item one"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        multiline_block = """1. Item one
2. Item two
3. Item three"""
        self.assertEqual(block_to_block_type(multiline_block), BlockType.ORDERED_LIST)

        error_block = """1. Item one
3. Item two
4. Item three"""
        self.assertNotEqual(block_to_block_type(error_block), BlockType.ORDERED_LIST)

        error2_block = """1. Item one
Not a list item
3. Item three"""
        self.assertNotEqual(block_to_block_type(error2_block), BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        block = "This is a regular paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        multiline_not_quote_block = (
            ">This is a quote but the next line isn't\nNot a quote"
        )
        self.assertEqual(
            block_to_block_type(multiline_not_quote_block), BlockType.PARAGRAPH
        )


class TestMarkdownToHtml(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_valid_heading(self):
        markdown = "## Not this\n# Title\nMore text"
        self.assertEqual(extract_title(markdown), "Title")

    def test_no_heading(self):
        markdown = "No heading here\nJust text"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            extract_title("")


if __name__ == "__main__":
    unittest.main()
