import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = (block.strip() for block in blocks)
    blocks = filter(lambda block: block != "", blocks)
    return list(blocks)


def block_to_block_type(block_text):
    if re.match(r"#{1,6}", block_text) is not None:
        return BlockType.HEADING
    if block_text.startswith("```\n") and block_text.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in block_text.split("\n")):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block_text.split("\n")):
        return BlockType.UNORDERED_LIST
    if all(
        line.startswith(f"{line_num + 1}. ")
        for (line_num, line) in enumerate(block_text.split("\n"))
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
