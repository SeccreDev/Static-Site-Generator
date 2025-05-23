import re
from textnode import TextType, TextNode

def text_to_textnodes(text):
    """
    Convert raw markdown text into a list of TextNodes with appropriate types.

    The function processes formatting in the following order:
    bold (**), italic (_), code (`), image (![alt](src)), and link ([text](href)).

    Args:
        text (str): The input markdown text.

    Returns:
        list[TextNode]: A list of parsed TextNodes.
    """
    node = TextNode(text, TextType.NORMAL)
    new_nodes = split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([node], "**", TextType.BOLD), "_",  TextType.ITALIC), "`", TextType.CODE)
    new_nodes = split_nodes_link(split_nodes_image(new_nodes))
    return new_nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes based on a markdown delimiter (e.g., ** for bold).

    Args:
        old_nodes (list[TextNode]): Input list of text nodes.
        delimiter (str): The markdown delimiter.
        text_type (TextType): The type to assign to delimited text.

    Returns:
        list[TextNode]: List with delimiter-formatted text converted to separate TextNodes.

    Raises:
        ValueError: If a delimiter is unbalanced (odd number of sections).
    """
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
    """
    Convert markdown image syntax to TextNode instances of type IMAGE.

    Args:
        old_nodes (list[TextNode]): List of existing text nodes.

    Returns:
        list[TextNode]: Updated list with image markdown converted to image TextNodes.

    Raises:
        ValueError: If an image markdown section is improperly closed.
    """
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
    """
    Convert markdown link syntax to TextNode instances of type LINK.

    Args:
        old_nodes (list[TextNode]): List of existing text nodes.

    Returns:
        list[TextNode]: Updated list with link markdown converted to link TextNodes.

    Raises:
        ValueError: If a link markdown section is improperly closed.
    """
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
    """
    Extract all markdown images in the form ![alt](src).

    Args:
        text (str): The raw input text.

    Returns:
        list[tuple[str, str]]: A list of (alt, src) tuples for each image.
    """
    match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match

def extract_markdown_links(text):
    """
    Extract all markdown links in the form [text](href).

    Args:
        text (str): The raw input text.

    Returns:
        list[tuple[str, str]]: A list of (text, href) tuples for each image.
    """
    match = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match