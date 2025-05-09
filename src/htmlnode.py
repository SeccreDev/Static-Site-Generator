class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self):
        if self.props is None:
            return ""
        html = ""
        for key, value in self.props.items():
            html += f"{key}=" + f'"{value}" '
        return html

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props.items() == other.props.items()

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"