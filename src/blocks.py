import re
from enum import Enum

from htmlnode import ParentNode
from markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextType, TextNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(md):
    if not md:
        return []
    blocks = md.strip().split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block):
    if not block:
        return

    if re.match(r"^#{1,6} [^\s]", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif all(
        line.startswith(f"{i}. ") for i, line in enumerate(block.splitlines(), start=1)
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return ParentNode("div", [block_to_html_node(block) for block in blocks], None)


def text_to_children(text):
    if not text:
        return []

    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in textnodes]


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case _:
            raise ValueError("invalid block type")


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break

        if level + 1 >= len(block):
            raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    child = text_node_to_html_node(TextNode(text, TextType.TEXT))
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = block.split("\n")
    if not all(line.startswith(">") for line in lines):
        raise ValueError("invalid quote block")

    content = " ".join([line.lstrip(">").strip() for line in lines])
    return ParentNode("blockquote", text_to_children(content))


def unordered_list_to_html_node(block):
    return ParentNode(
        "ul",
        [ParentNode("li", text_to_children(item[2:])) for item in block.split("\n")],
    )


def ordered_list_to_html_node(block):
    return ParentNode(
        "ol",
        [ParentNode("li", text_to_children(item[3:])) for item in block.split("\n")],
    )


def paragraph_to_html_node(block):
    return ParentNode("p", text_to_children(" ".join(block.split("\n"))))
