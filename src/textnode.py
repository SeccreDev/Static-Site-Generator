import re
from enum import Enum, auto
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, text_node.url)
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unitendified text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
        else:        
            split_nodes = []
            sections = old_node.text.split(delimiter)

            if len(sections) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], TextType.NORMAL))
                else:
                    split_nodes.append(TextNode(sections[i], text_type))
            new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    # my first regex ;(  r"\!\[(.*?)\]\((.*?)\)"
    match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match

def extract_markdown_links(text):
    # my second regex :( r"\[(.*?)\]\((.*?)\)"
    match = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
        else:
            original_text = old_node.text
            extracted_images = extract_markdown_images(original_text)
            if not extracted_images:
                new_nodes.append(old_node)
            else:
                for extracted_image in extracted_images:  #FIX: If section[0] == "" it wont add the TextNode("", image, url)
                    sections = original_text.split(f"![{extracted_image[0]}]({extracted_image[1]})", 1)
                    if len(sections) != 2:
                        raise ValueError("invalid markdown, image section not closed")
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                        new_nodes.append(TextNode(extracted_image[0], TextType.IMAGE, extracted_image[1]))
                        original_text = sections[1]
                if (original_text != ""):
                    new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
        else:
            original_text = old_node.text
            extracted_links = extract_markdown_links(original_text)
            if not extracted_links:
                new_nodes.append(old_node)
            else:
                for extracted_link in extracted_links:  #FIX: If section[0] == "" it wont add the TextNode("", link, url)
                    sections = original_text.split(f"[{extracted_link[0]}]({extracted_link[1]})", 1)
                    if len(sections) != 2:
                        raise ValueError("invalid markdown, link section not closed")
                    if sections[0] != "":
                        new_nodes.append(TextNode(sections[0], TextType.NORMAL))
                        new_nodes.append(TextNode(extracted_link[0], TextType.LINK, extracted_link[1]))
                        original_text = sections[1]
                if (original_text != ""):
                    new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes