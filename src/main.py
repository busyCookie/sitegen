from textnode import TextType, TextNode
from htmlnode import HTMLNode
from utilities import refesh_content, generate_pages_recursive

import sys

def main():
    if sys.argv[1]:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    refesh_content("./static/", "./docs/")
    generate_pages_recursive("./content/", "./template.html", "./docs/", basepath)

if __name__ == "__main__":
    main()
