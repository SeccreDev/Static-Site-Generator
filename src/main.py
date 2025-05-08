from textnode import *

def main():
    text_node = TextNode("Anchor text", TextType.LINK, "github.com")
    print(text_node)
    # print(f"Is text_node equal to text_node2: {text_node == text_node2}")

main()