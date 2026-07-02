from htmlnode import HTMLNode,ParentNode,LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes
from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        block_strip = block.strip()
        if block_strip != "":
            stripped_blocks.append(block_strip)
    return stripped_blocks
    
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    lines = block.split("\n")
    if lines[0].startswith("```") and lines[-1].startswith("```") and len(lines) > 1:
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    if block.startswith("1. "):
        i = 0
        for line in lines:
            i+= 1
            if not line.startswith(str(i) + ". "):
                return BlockType.PARAGRAPH
        return BlockType.OLIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def paragraph_to_html(block):
    html_nodes = text_to_children(block.replace("\n", " "))
    return ParentNode("p",html_nodes)

def heading_to_html(block):
    heading_level = 0
    for char in block:
        if char == "#":
            heading_level+= 1
        else:
            break
    html_nodes = text_to_children(block[heading_level + 1:])
    return ParentNode("h" + str(heading_level), html_nodes)

def quote_to_html(block):
    lines = block.split("\n")
    stripped_lines = [line.lstrip(">").strip() for line in lines]
    new_block = " ".join(stripped_lines)
    html_nodes = text_to_children(new_block)
    return ParentNode("blockquote", html_nodes)

def code_to_html(block):
    extracted_text = block[4:-3]
    text_node = TextNode(extracted_text,TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    parent_node = ParentNode("code", [html_node])
    return ParentNode("pre", [parent_node])

def ulist_to_html(block):
    lines = block.split("\n")
    stripped_lines = [line[2:] for line in lines]
    line_nodes = []
    for line in stripped_lines:
        html_nodes = text_to_children(line)
        parent_node = ParentNode("li", html_nodes)
        line_nodes.append(parent_node)
    return ParentNode("ul", line_nodes)

def olist_to_html(block):
    lines = block.split("\n")
    stripped_lines = [line.split(". ", 1)[1] for line in lines]
    line_nodes = []
    for line in stripped_lines:
        html_nodes = text_to_children(line)
        parent_node = ParentNode("li", html_nodes)
        line_nodes.append(parent_node)
    return ParentNode("ol", line_nodes)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html(block)
        case BlockType.HEADING:
            return heading_to_html(block)
        case BlockType.CODE:
            return code_to_html(block)
        case BlockType.QUOTE:
            return quote_to_html(block)
        case BlockType.ULIST:
            return ulist_to_html(block)
        case BlockType.OLIST:
            return olist_to_html(block)
        case _:
            raise ValueError("Unidentified block type")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in blocks:
        html_block = block_to_html_node(block)
        html_blocks.append(html_block)
    return ParentNode("div", html_blocks)