import re
from enum import Enum

from htmlnode import LeafNode, ParentNode
from text_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node


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


def markdown_to_html_node(markdown):
    def text_to_children(text):
        text_nodes = text_to_textnodes(text)
        return [text_node_to_html_node(node) for node in text_nodes]

    html_nodes = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_nodes.append(
                    ParentNode("p", text_to_children(block.replace("\n", " ")))
                )
            case BlockType.HEADING:
                numHeading = 0
                while block[numHeading] == "#":
                    numHeading += 1
                html_nodes.append(ParentNode(f"h{numHeading}", text_to_children(block)))
            case BlockType.CODE:
                text = block[4:-3]  # remove "```\n"
                html_nodes.append(ParentNode("pre", [LeafNode("code", text)]))
            case BlockType.QUOTE:
                html_nodes.append(ParentNode("blockquote", text_to_children(block)))
            case BlockType.UNORDERED_LIST:
                items_text = [line[2:] for line in block]  # remove "- "
                items_nodes = [LeafNode("li", text) for text in items_text]
                html_nodes.append(ParentNode("ul", items_nodes))
            case BlockType.ORDERED_LIST:
                items_text = [
                    line.split(".", maxsplit=1)[1][1:] for line in block
                ]  # remove "{num}. "
                items_nodes = [LeafNode("li", text) for text in items_text]
                html_nodes.append(ParentNode("ol", items_nodes))

    return ParentNode("div", html_nodes)
