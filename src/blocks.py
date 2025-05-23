import re
from enum import Enum
from inline_markdown import *
from htmlnode import *
from textnode import text_node_to_html_node

class BlockType(Enum):
    """Enumeration for different markdown block types."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    """
    Split markdown content into distinct blocks.

    Blocks are separated by double newlines.

    Args:
        markdown (str): The raw markdown string.

    Returns:
        list[str]: List of cleaned, non-empty block strings.
    """
    filtered_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block:
            filtered_blocks.append(block)
    return filtered_blocks
    
def block_to_block_type(block):
    """
    Identify the type of a given markdown block.

    Args:
        block (str): The markdown block string.

    Returns:
        BlockType: The corresponding block type enum.
    """
    split_lines = block.splitlines()
    heading_match = all(re.match(r"^#{1,6} ", line) for line in split_lines)
    code_match = re.match(r"(?s)^```.*?```$", block)
    quote_match = all(re.match(r"^>", line) for line in split_lines)
    unordered_match = all(re.match(r"^- ", line) for line in split_lines)
    ordered_match = all(re.match(rf"^{i}*\. ", line) for i, line in enumerate(split_lines, 1))

    if heading_match:
        return BlockType.HEADING
    elif code_match:
        return BlockType.CODE
    elif quote_match:
        return BlockType.QUOTE
    elif unordered_match:
        return BlockType.UNORDERED_LIST
    elif ordered_match:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    """
    Convert full markdown content to a tree of HTML nodes.

    Args:
        markdown (str): The markdown content.

    Returns:
        ParentNode: A 'div' parent node containing HTML children.
    """
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        parent_node = block_to_parent_node(block)
        children.append(parent_node)
    return ParentNode("div", children)

def block_to_parent_node(block):
    """
    Convert a markdown block to the appropriate HTML ParentNode.

    Args:
        block (str): A markdown block.

    Returns:
        ParentNode: HTML representation of the markdown block.
    """
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph = " ".join(lines)
            childrens = text_to_childrens(paragraph)
            return ParentNode("p", childrens)

        case BlockType.HEADING:
            if block.startswith("# "):
                childrens = text_to_childrens(block[2:])
                return ParentNode("h1", childrens)
            elif block.startswith("## "):
                childrens = text_to_childrens(block[3:])
                return ParentNode("h2", childrens)
            elif block.startswith("### "):
                childrens = text_to_childrens(block[4:])
                return ParentNode("h3", childrens)
            elif block.startswith("#### "):
                childrens = text_to_childrens(block[5:])
                return ParentNode("h4", childrens)
            elif block.startswith("##### "):
                childrens = text_to_childrens(block[6:])
                return ParentNode("h5", childrens)
            else:
                childrens = text_to_childrens(block[7:])
                return ParentNode("h6", childrens)

        case BlockType.CODE:
            text = block[4:-3]
            textnode = TextNode(text, TextType.NORMAL)
            children = text_node_to_html_node(textnode)
            return ParentNode("pre", [ParentNode("code", [children])])
            
        case BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            childrens = text_to_childrens(content)
            return ParentNode("blockquote", childrens)

        case BlockType.UNORDERED_LIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[2:]
                children = text_to_childrens(text)
                html_items.append(ParentNode("li", children))
            return ParentNode("ul", html_items)

        case BlockType.ORDERED_LIST:
            items = block.split("\n")
            html_items = []
            for item in items:
                text = item[item.find(".") + 2:]
                children = text_to_childrens(text)
                html_items.append(ParentNode("li", children))
            return ParentNode("ol", html_items)    

        case _:
            raise ValueError("Not a valid BlockType")


def text_to_childrens(block):
    """
    Convert text into a list of HTML leaf nodes based on inline markdown.

    Args:
        block (str): The raw inline text.

    Returns:
        list[LeafNode]: List of HTML leaf nodes derived from the text.
    """
    textnodes = text_to_textnodes(block)
    childrens = []
    
    for textnode in textnodes:
        childrens.append(text_node_to_html_node(textnode))
    
    return childrens