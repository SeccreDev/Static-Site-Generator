class HTMLNode():
    """Base class for HTML nodes. Can represent a tag with optional value, children, and properties."""

    def __init__(self, tag = None, value = None, children = None, props = None):
        """
        Initialize an HTMLNode instance.

        Args:
            tag (str, optional): The HTML tag.
            value (str, optional): The text content.
            children (list, optional): List of child HTMLNode objects.
            props (dict, optional): HTML attributes as key-value pairs.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        """
        Convert this node to an HTML string.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self):
        """
        Convert props dictionary to a string of HTML attributes.

        Returns:
            str: HTML attributes in the form ' key="value"' (with leading space).
        """
        if self.props is None:
            return ""
        html = ""
        for key, value in self.props.items():
            html += f" {key}=" + f'"{value}"'
        return html

    def __eq__(self, other):
        """
        Compare this node with another HTMLNode for equality.

        Args:
            other (HTMLNode): The node to compare with.

        Returns:
            bool: True if equal, False otherwise.
        """
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props.items() == other.props.items()

    def __repr__(self):
        """
        Return a string representation of the HTMLNode.

        Returns:
            str: String representation.
        """
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    """
    Represents a leaf node in the HTML tree (i.e., a tag with no children but with a value).
    """

    def __init__(self, tag, value, props=None):
        """
        Initialize a LeafNode instance.

        Args:
            tag (str): The HTML tag.
            value (str): The text content.
            props (dict, optional): HTML attributes as key-value pairs.
        """
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        """
        Convert the leaf node to an HTML string.

        Returns:
            str: The HTML representation of the leaf node.

        Raises:
            ValueError: If the value is None.
        """
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        """
        Return a string representation of the LeafNode.

        Returns:
            str: String representation.
        """
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    """
    Represents a parent node in the HTML tree (i.e., a tag with children but no direct value).
    """

    def __init__(self, tag, children, props=None):
        """
        Initialize a ParentNode instance.

        Args:
            tag (str): The HTML tag.
            children (list[HTMLNode]): List of child nodes.
            props (dict, optional): HTML attributes as key-value pairs.
        """
        super().__init__(tag, None, children, props)

    def to_html(self):
        """
        Convert the parent node and its children to an HTML string.

        Returns:
            str: The HTML representation of the parent node.

        Raises:
            ValueError: If tag or children are missing.
        """
        html = ""
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have children")
        else:
            html = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                html += child.to_html()
            html += f"</{self.tag}>"
        return html
    
    def __eq__(self, other):
        """
        Compare this node with another ParentNode for equality.

        Args:
            other (ParentNode): The node to compare with.

        Returns:
            bool: True if equal, False otherwise.
        """
        if not isinstance(other, ParentNode):
            return NotImplemented
        if self.props is None:
            return self.tag == other.tag and self.children == other.children
        else:
            return self.tag == other.tag and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        """
        Return a string representation of the ParentNode.

        Returns:
            str: String representation.
        """
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

