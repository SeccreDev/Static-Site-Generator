from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    """Enumeration of possible text types for a text node."""
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    """Represents a node containing text and its formatting type."""
    
    def __init__(self, text, text_type, url=None):
        """
        Initialize a TextNode instance.

        Args:
            text (str): The text content.
            text_type (TextType): The type of the text (e.g., bold, italic, link).
            url (str, optional): The URL for links or images. Defaults to None.
        """
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        """
        Compare this TextNode with another for equality.

        Args:
            other (TextNode): Another instance to compare.

        Returns:
            bool: True if both instances are equal, False otherwise.
        """
        if not isinstance(other, TextNode):
            return NotImplemented
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        """
        Return a string representation of the TextNode.

        Returns:
            str: String representation.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    """
    Convert a TextNode to a corresponding LeafNode for HTML rendering.

    Args:
        text_node (TextNode): The TextNode to convert.

    Returns:
        LeafNode: An HTML representation of the text node.

    Raises:
        ValueError: If the text type is not recognized.
    """
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
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unidentified text type: {text_node.text_type}")