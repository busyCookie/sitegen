import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utilities import text_node_to_html_node, split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_link, split_nodes_image


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

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://localhost:8080/)")

        self.assertListEqual(matches, [("link", "https://localhost:8080/")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")

        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
