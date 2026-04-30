from textnode import TextType, TextNode
from htmlnode import HTMLNode
from utilities import text_to_textnodes

def main():
    tnode = TextNode("Text", TextType.LINK, "https://localhost:8080/")
    print(f"{tnode}")

    htmlprops = {
        "href": "https://localhost:8080/",
        "target": "_blank"
        }

    hnode = HTMLNode("<a>", "This is a html node", htmlprops)
    print(f"{hnode}")

    text_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

    print(text_nodes)

if __name__ == "__main__":
    main()
