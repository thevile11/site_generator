from htmlnode import HTMLNode
from textnode import TextNode, TextType
from enum import Enum
from find_regex import extract_markdown_images,extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            splitted_nodes = node.text.split(delimiter)
            if len(splitted_nodes) % 2 == 0:
                raise ValueError("Delimeter not closed")
            for piece in range(len(splitted_nodes)):
                if splitted_nodes[piece] == "":
                    continue
                if piece % 2 == 0:
                    new_nodes.append(TextNode(splitted_nodes[piece],TextType.TEXT))
                else:
                    new_nodes.append(TextNode(splitted_nodes[piece],text_type))
    return new_nodes     

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            extracted_images = extract_markdown_images(node.text)
            if len(extracted_images) != 0:
                remaining = node.text
                for ex_text, ex_url in extracted_images:
                    splitted = remaining.split(f"![{ex_text}]({ex_url})", 1)
                    if splitted[0] != "":
                        new_nodes.append(TextNode(splitted[0], TextType.TEXT))
                    new_nodes.append(TextNode(ex_text,TextType.IMAGE,ex_url))
                    remaining = splitted[1]
                if remaining != "":
                    new_nodes.append(TextNode(remaining,TextType.TEXT))
            else:
                new_nodes.append(node)
    return new_nodes  

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            extracted_links = extract_markdown_links(node.text)
            if len(extracted_links) != 0:
                remaining = node.text
                for ex_text, ex_url in extracted_links:
                    splitted = remaining.split(f"[{ex_text}]({ex_url})", 1)
                    if splitted[0] != "":
                        new_nodes.append(TextNode(splitted[0], TextType.TEXT))
                    new_nodes.append(TextNode(ex_text,TextType.LINK,ex_url))
                    remaining = splitted[1]
                if remaining != "":
                    new_nodes.append(TextNode(remaining,TextType.TEXT))
            else:
                new_nodes.append(node)
    return new_nodes            

def text_to_textnodes(text):
    input_node = TextNode(text,TextType.TEXT)
    first_split = split_nodes_delimiter([input_node],"**",TextType.BOLD)
    second_split = split_nodes_delimiter(first_split, "_", TextType.ITALIC)
    third_split = split_nodes_delimiter(second_split,"`",TextType.CODE)
    fourth_split = split_nodes_image(third_split)
    fifth_split = split_nodes_link(fourth_split)
    return fifth_split 


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

def block_to_block_type(block: str):
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