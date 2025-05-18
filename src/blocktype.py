import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    split_lines = block.splitlines()
    heading_match = all(re.match(r"^#{1,6} ", line) for line in split_lines)
    code_match = re.match(r"(?s)^```.*?```$", block)
    quote_match = all(re.match(r"^> ", line) for line in split_lines)
    unordered_match = all(re.match(r"^- ", line) for line in split_lines)
    ordered_match = all(re.match(rf"^{i}*\. ", line) for i, line in enumerate (split_lines, 1))

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