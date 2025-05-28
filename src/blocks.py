from enum import Enum
import re


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

    if re.match(r'^#{1,6} [^\s]', block):
        return BlockType.HEADING
    elif block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    elif all(line.startswith('>') for line in block.splitlines()):
        return BlockType.QUOTE
    elif all(line.startswith('- ') for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f'{i}. ') for i, line in enumerate(block.splitlines(), start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
