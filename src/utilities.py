import re

from textnode import TextType, TextNode
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            new_node = LeafNode(None, text_node.text)

        case TextType.BOLD:
            new_node = LeafNode("b", text_node.text)

        case TextType.ITALIC:
            new_node = LeafNode("i", text_node.text)

        case TextType.CODE:
            new_node = LeafNode("code", text_node.text)

        case TextType.LINK:
            props = {}
            props["href"] = text_node.url

            new_node = LeafNode("a", text_node.text, props)

        case TextType.IMG:
            props = {}
            props["src"] = text_node.url
            props["alt"] = text_node.text

            new_node = LeafNode("img", None, props)

        case _:
            raise Exception("Invalid TextNode type")

    return new_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        elif node.text.count(delimiter) == 0:
            new_nodes.append(node)

        elif node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid markdown syntax: last {delimiter} is not closed")

        else:
            parts = node.text.split(delimiter)

            for i in range(0, len(parts)-1, 2):
                new_text_node = TextNode(parts[i], TextType.TEXT)
                new_typed_node = TextNode(parts[i + 1], text_type)

                new_nodes.append(new_text_node)
                new_nodes.append(new_typed_node)

            if parts[-1] != "":
                new_nodes.append(TextNode(parts[-1], TextType.TEXT))

    return new_nodes

def extract_markdown_lnks(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return links

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return images

