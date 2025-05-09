from textnode import *
from htmlnode import *

def main():
    text_node = TextNode("Anchor text", TextType.LINK, "github.com")
    print(text_node)
    html_node = HTMLNode("h", "This is a heading", None, {"href": "https://www.google.com", "target": "_blank",})
    print(html_node)

main()