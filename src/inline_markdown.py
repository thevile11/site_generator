from htmlnode import HTMLNode
from textnode import TextNode, TextType

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


