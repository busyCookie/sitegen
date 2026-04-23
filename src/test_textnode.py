import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node1, node2)

    def test_eq_nonlink(self):
        node1 = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq_link(self):
        node1 = TextNode("This is a text node", TextType.ITALIC, "https://localhost:8080/")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://localhost:8080/")
        self.assertEqual(node1, node2)

    def test_difftext(self):
        node1 = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a different text node", TextType.CODE)
        self.assertNotEqual(node1, node2)

    def test_difftype(self):
        node1 = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.IMG)
        self.assertNotEqual(node1, node2)

    def test_difflink(self):
        node1 = TextNode("This is a text node", TextType.ITALIC, "https://localhost:8080/")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://host:8080/")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        control = "TextNode(Text, link, https://localhost:8080/)"
        node = TextNode("Text", TextType.LINK, "https://localhost:8080/")
        representation = str(node)

        self.assertEqual(representation, control)



if __name__ == "__main__":
    unittest.main()
