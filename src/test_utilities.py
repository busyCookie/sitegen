import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utilities import text_node_to_html_node, split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_link, split_nodes_image, text_to_textnodes, markdown_to_blocks


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

    def test_text_proccess(self):
        control = [TextNode("This is ", TextType.TEXT),
                   TextNode("text", TextType.BOLD),
                   TextNode(" with an ", TextType.TEXT),
                   TextNode("italic", TextType.ITALIC),
                   TextNode(" word and a ", TextType.TEXT),
                   TextNode("code block", TextType.CODE),
                   TextNode(" and an ", TextType.TEXT),
                   TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
                   TextNode("link", TextType.LINK, "https://boot.dev")
                   ]
        extract_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

        self.assertListEqual(control, extract_nodes)

    def test_markdown_to_blocks(self):
        control = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"]

        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(blocks, control)
