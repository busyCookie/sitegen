from textnode import TextType, TextNode
from htmlnode import HTMLNode
from utilities import text_to_textnodes, refesh_content

def main():
    refesh_content("./static/", "./public/")

if __name__ == "__main__":
    main()
