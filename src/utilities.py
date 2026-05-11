import re
import os
import shutil

from textnode import TextType, BlockType, TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def refesh_content(src, dest):
    if not os.path.exists(src):
        raise Exception(f"source directory does not exists: {src}")

    clean_target(dest)

    copy_content(src, dest)

def clean_target(dest):
    if re.match("^[a-zA-Z]:\\)*", dest):
        dest = dest[2:]
    if dest[0] == "/":
        dest = f".{dest}"

    if os.path.exists(dest):
        if os.path.isfile(dest):
            os.remove(dest)

        else:
            dir_content = os.listdir(dest)

            for item in dir_content:
                clean_target(os.path.join(dest, item))

            os.rmdir(dest)

def copy_content(src, dest):
    if not os.path.exists(src):
        raise Exception(f"source directory does not exists: {src}")
    if os.path.exists(dest):
        raise Exception(f"target directory already exists: {src}")

    if os.path.isfile(src):
        shutil.copy(src, dest)

    else:
        os.mkdir(dest)

        dir_content = os.listdir(src)

        for item in dir_content:
            src_sub = os.path.join(src, item)
            dest_sub = os.path.join(dest, item)

            copy_content(src_sub, dest_sub)

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            new_node = LeafNode(None, text_node.text)

        case TextType.BOLD:
            new_node = LeafNode("b", text_node.text)

        case TextType.ITALIC:
            new_node = LeafNode("i", text_node.text)

        case TextType.CODE:
            new_node = LeafNode("code", text_node.text)

        case TextType.LINK:
            props = {}
            props["href"] = text_node.url

            new_node = LeafNode("a", text_node.text, props)

        case TextType.IMG:
            props = {}
            props["src"] = text_node.url
            props["alt"] = text_node.text

            new_node = LeafNode("img", None, props)

        case _:
            raise Exception("Invalid TextNode type")

    return new_node

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")

    processed_blocks = []
    for block in raw_blocks:
        processed_block = block.strip("\n")
        while (processed_block.startswith(" ") or processed_block.startswith("\n") or processed_block.endswith(" ") or processed_block.endswith("\n") ):
            processed_block = processed_block.strip()
            processed_block = processed_block.strip("\n")

        if processed_block != "":
            processed_blocks.append(processed_block)

    return processed_blocks

def block_to_block_type(block):

    if re.match(r"\#{1,6} \w+", block):
        return BlockType.HEAD

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    quote = True
    ulist = True
    olist = True
    olist_count = 1
    lines = block.splitlines()

    for line in lines:
        if quote and not line.startswith(">"):
            quote = False
        if ulist and not line.startswith("- "):
            ulist = False
        if olist and not line.startswith(f"{olist_count}. "):
            olist = False
        olist_count += 1

    if quote:
        return BlockType.QUOTE
    if ulist:
        return BlockType.ULIST
    if olist:
        return BlockType.OLIST

    return BlockType.PAR


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        elif node.text.count(delimiter) == 0:
            new_nodes.append(node)

        elif node.text.count(delimiter) % 2 != 0:
            raise Exception(f"Invalid markdown syntax: last {delimiter} is not closed")

        else:
            parts = node.text.split(delimiter)

            for i in range(0, len(parts)-1, 2):
                new_text_node = TextNode(parts[i], TextType.TEXT)
                new_typed_node = TextNode(parts[i + 1], text_type)

                new_nodes.append(new_text_node)
                new_nodes.append(new_typed_node)

            if parts[-1] != "":
                new_nodes.append(TextNode(parts[-1], TextType.TEXT))

    return new_nodes

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return links

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

    return images

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text == "":
            continue

        workline = node.text
        links = extract_markdown_links(workline)

        if node.text_type != TextType.TEXT or links == []:
            new_nodes.append(node)

        else:
            for link in links:
                parts = workline.split(f"[{link[0]}]({link[1]})", 1)

                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))

                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

                workline = parts[1]

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text == "":
            continue

        workline = node.text
        images = extract_markdown_images(workline)

        if node.text_type != TextType.TEXT or images == []:
            new_nodes.append(node)

        else:
            for image in images:
                parts = workline.split(f"![{image[0]}]({image[1]})", 1)

                if parts[0] != "":
                    new_nodes.append(TextNode(parts[0], TextType.TEXT))

                new_nodes.append(TextNode(image[0], TextType.IMG, image[1]))

                workline = parts[1]

    return new_nodes

def text_to_textnodes(text):
    nodes = split_nodes_link([TextNode(text, TextType.TEXT)])
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)

    return nodes

def markdown_to_html_node(markdown):
    html_tree = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        type = block_to_block_type(block)
        match type:
            case BlockType.PAR:
                html_children = []
                block = block.replace("\n", " ")
                while block.count("  ") > 0:
                    block.replace("  ", " ")
                text_nodes = text_to_textnodes(block)
                for text_node in text_nodes:
                    html_children.append(text_node_to_html_node(text_node))

                html_tree.append(ParentNode("p", html_children))

            case BlockType.QUOTE:
                html_children = []
                text_nodes = text_to_textnodes(block)
                for text_node in text_nodes:
                    html_children.append(text_node_to_html_node(text_node))

                html_tree.append(ParentNode("blockquote", html_children))

            case BlockType.OLIST:
                lines = text_nodes.splitlines()
                html_lines = []
                for line in lines:
                    html_line_children = []
                    line = line.split(". ", 1)[1]
                    line_nodes = text_to_textnodes(line)

                    for line_node in line_nodes:
                        html_line_children.append(text_node_to_html_node(line_node))

                    html_lines.appen(ParentNode("li", html_line_children ))

                html_tree.append(ParentNode("ol", html_lines))

            case BlockType.ULIST:
                lines = text_nodes.splitlines()
                html_lines = []
                for line in lines:
                    html_line_children = []
                    line = line[2:]
                    line_nodes = text_to_textnodes(line)

                    for line_node in line_nodes:
                        html_line_children.append(text_node_to_html_node(line_node))

                    html_lines.appen(ParentNode("li", html_line_children ))

                html_tree.append(ParentNode("ul", html_lines))

            case BlockType.HEAD:
                hlevel = block.count("#")
                html_tree.append(LeafNode(f"h{hlevel}", block[hlevel+1:]))

            case BlockType.CODE:
                text = block[3:].strip()
                text = text[:-3]
                html_tree.append(ParentNode("pre", [LeafNode("code", text)]))

            case _:
                raise Exception("Invalid BlocNode type")

    return ParentNode("div", html_tree)


