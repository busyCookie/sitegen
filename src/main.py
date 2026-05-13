from textnode import TextType, TextNode
from htmlnode import HTMLNode
from utilities import refesh_content, generate_pages_recursive

def main():
    refesh_content("./static/", "./public/")
    generate_pages_recursive("./content/", "./template.html", "./public/")

if __name__ == "__main__":
    main()
