import unittest

from textnode import TextNode, TextType, BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from utilities import text_node_to_html_node, split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_link, split_nodes_image, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestBlockProcessing(unittest.TestCase):

    def test_markdown_to_single_block(self):
        control = [
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."]

        md = ("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.")

        blocks = markdown_to_blocks(md)

        self.assertListEqual(blocks, control)

    def test_markdown_to_block_traling_spaces(self):
        control = [
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book."]

        md = ("  \n\n  Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. \n\n ")

        blocks = markdown_to_blocks(md)

        self.assertListEqual(blocks, control)

    def test_markdown_to_block_newlines(self):
        control = [
            "Lorem Ipsum is simply dummy text of the printing and typesetting industry.\nLorem Ipsum has been the industry's standard dummy text ever since the 1500s,\nwhen an unknown printer took a galley of type and scrambled it to make a type specimen book."]

        md = ("Lorem Ipsum is simply dummy text of the printing and typesetting industry.\nLorem Ipsum has been the industry's standard dummy text ever since the 1500s,\nwhen an unknown printer took a galley of type and scrambled it to make a type specimen book.")

        blocks = markdown_to_blocks(md)

        self.assertListEqual(blocks, control)

    def test_markdown_to_blocks(self):
        control = [
            "##Test Data",
            "This is a paragraph with **bolded** text. And an additional sentence.",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"]

        md = ("##Test Data\n\n"
            "This is a paragraph with **bolded** text. And an additional sentence.\n\n"
            "This is another paragraph with _italic_ text and `code` here\n"
            "This is the same paragraph on a new line\n\n"
            "- This is a list\n"
            "- with items\n")

        blocks = markdown_to_blocks(md)

        self.assertListEqual(blocks, control)

    def test_header_block(self):
        control = BlockType.HEAD
        block = "### Header"

        block_type = block_to_block_type(block)

        self.assertEqual(control, block_type)

    def test_code_block(self):
        control = BlockType.CODE
        block = ("```\n"
            "def code_block(self):\n"
            "code.execute(parameters)\n"
            "```")

        block_type = block_to_block_type(block)

        self.assertEqual(control, block_type)

    def test_quote_block(self):
        control = BlockType.QUOTE
        block = (">samurai without the sword\n"
            ">is the same as with the sword\n"
            ">but without the sword.\n")

        block_type = block_to_block_type(block)

        self.assertEqual(control, block_type)

    def test_ulist_block(self):
        control = BlockType.ULIST
        block = ("- order the list\n"
            "- make unorderd list\n"
            "- take a new list\n")

        block_type = block_to_block_type(block)

        self.assertEqual(control, block_type)


    def test_olist_block(self):
        control = BlockType.OLIST
        block = ("1. Take a new list.\n"
            "2. Make unorderd list.\n"
            "3. Order the list.\n")

        block_type = block_to_block_type(block)

        self.assertEqual(control, block_type)

    def test_header_block(self):
        control = BlockType.PAR
        block = ("Just some regualr paragraph of text.\n"
            "With two lines, mardown does not care for.")

        block_type = block_to_block_type(block)

        self.assertEqual(control, block_type)

    def test_not_quote_block(self):
        control = BlockType.QUOTE
        block = (">samurai without the sword\n"
            ">is the same as with the sword\n"
            "-but without the sword.\n")

        block_type = block_to_block_type(block)

        self.assertNotEqual(control, block_type)

    def test_wronglist0_block(self):
        control = BlockType.ULIST
        block = ("- order the list\n"
            "2. make unorderd list\n"
            "* take a new list\n")

        block_type = block_to_block_type(block)

        self.assertNotEqual(control, block_type)

    def test_wronglist0_block(self):
        control = BlockType.ULIST
        block = ("1. order the list\n"
            "2. make unorderd list\n"
            "- take a new list\n")

        block_type = block_to_block_type(block)

        self.assertNotEqual(control, block_type)

#class TestLineProcessing(unittest.TestCase):

#class TestHTMLGeneration(unittest.TestCase):


class TestUtilities(unittest.TestCase):

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://localhost:8080/)")

        self.assertListEqual(matches, [("link", "https://localhost:8080/")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")

        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_split_bold(self):
        control = [TextNode("This is ", TextType.TEXT), TextNode("a bold text", TextType.BOLD), TextNode(" node", TextType.TEXT)]
        node = TextNode("This is **a bold text** node", TextType.TEXT)
        node_list = []
        node_list.append(node)

        nodes = split_nodes_delimiter(node_list, "**", TextType.BOLD)

        self.assertEqual(nodes, control, msg=f"{0}, {1}")


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


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual( html, "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")


    def test_codeblock(self):
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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
