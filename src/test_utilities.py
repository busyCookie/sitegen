import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utilities import text_node_to_html_node, split_nodes_delimiter


class TestUtilities(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_bold(self):
        control = [TextNode("This is ", TextType.TEXT), TextNode("a bold text", TextType.BOLD), TextNode(" node", TextType.TEXT)]
        node = TextNode("This is **a bold text** node", TextType.TEXT)
        node_list = []
        node_list.append(node)

        nodes = split_nodes_delimiter(node_list, "**", TextType.BOLD)

        self.assertEqual(nodes, control, msg=f"{0}, {1}")
