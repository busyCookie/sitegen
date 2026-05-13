from textnode import TextType, TextNode
from htmlnode import HTMLNode
from utilities import refesh_content, generate_page

def main():
    refesh_content("./static/", "./public/")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

if __name__ == "__main__":
    main()
