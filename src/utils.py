import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Incorrect Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if delimiter not in ["**", "_", "`"]:
        raise ValueError("wrong delimiter")

    delimiter_to_type = {
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
        "`": TextType.CODE,
    }

    if text_type != delimiter_to_type.get(delimiter):
        raise ValueError(
            f"Delimiter '{delimiter}' does not match text type '{text_type.value}'. "
            f"Expected '{delimiter}' for '{delimiter_to_type[delimiter]}'."
        )

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("unmatching delimiter")

        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.extend([TextNode(part, TextType.TEXT)])
            else:
                new_nodes.extend([TextNode(part, text_type)])

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(node.text) == 0:
            continue

        parts = re.split(r"(!\[.*?\]\(.*?\))", node.text)

        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.extend([TextNode(part, TextType.TEXT)])
            else:
                image_text, image_url = extract_markdown_images(part)[0]
                new_nodes.extend(
                    [TextNode(image_text or "", TextType.IMAGE, image_url or "")]
                )

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(node.text) == 0:
            continue

        parts = re.split(r"(\[.*?\]\(.*?\))", node.text)

        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.extend([TextNode(part, TextType.TEXT)])
            else:
                link_text, link_url = extract_markdown_links(part)[0]
                new_nodes.extend(
                    [TextNode(link_text or "", TextType.LINK, link_url or "")]
                )

    return new_nodes
