import re
from textnode import TextType, TextNode

def text_to_textnodes(text):
    node = TextNode(text, TextType.NORMAL)
    new_nodes = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([node], "**", TextType.BOLD), "_",  TextType.ITALIC), "`", TextType.CODE)
    new_nodes = split_nodes_link(split_nodes_image(new_nodes))
    return new_nodes

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
                for extracted_image in extracted_images:
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
                for extracted_link in extracted_links:
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

def extract_markdown_images(text):
    # my first regex ;(  r"\!\[(.*?)\]\((.*?)\)"
    match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match

def extract_markdown_links(text):
    # my second regex :( r"\[(.*?)\]\((.*?)\)"
    match = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match