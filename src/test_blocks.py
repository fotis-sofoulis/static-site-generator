from blocks import markdown_to_blocks
import unittest


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
            "Third block"
        ]
        self.assertEqual(markdown_to_blocks(md), expected)
