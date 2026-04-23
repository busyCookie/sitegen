from textnode import TextType, TextNode
from htmlnode import HTMLNode

def main():
    tnode = TextNode("Text", TextType.LINK, "https://localhost:8080/")
    print(f"{tnode}")

    htmlprops = {
        "href": "https://localhost:8080/",
        "target": "_blank"
        }

    hnode = HTMLNode("<a>", "This is a html node", htmlprops)
    print(f"{hnode}")

if __name__ == "__main__":
    main()
