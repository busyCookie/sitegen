from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMG = "image"

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


class TextNode:
    def __init__(self, text, text_type, url = None):

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
