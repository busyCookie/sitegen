import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_empty(self):
        node = HTMLNode()

        self.assertTrue(node)

    def test_eq(self):
        htmlprops = {
            "href": "https://localhost:8080/",
            "target": "_blank"
        }
        node1 = HTMLNode("<a>", "This is a html node", htmlprops)
        node2 = HTMLNode("<a>", "This is a html node", htmlprops)

        self.assertEqual(node1, node2)

    def test_difftag(self):
        htmlprops = {
            "href": "https://localhost:8080/",
            "target": "_blank"
            }
        node1 = HTMLNode("<a>", "This is a html node", htmlprops)
        node2 = HTMLNode("<p>", "This is a html node", htmlprops)

        self.assertNotEqual(node1, node2)

    def test_repr(self):
        htmlprops = {
            "href": "https://localhost:8080/",
            "target": "_blank"
            }
        control = "HTMLNode(<a>, This is a html node, None, {'href': 'https://localhost:8080/', 'target': '_blank'})"

        node = HTMLNode("<a>", "This is a html node", htmlprops)
        representation = str(node)

        self.assertEqual(representation, control)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
            )


if __name__ == "__main__":
    unittest.main()
