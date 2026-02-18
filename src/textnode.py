from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    REGULAR = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({repr(self.text)}, {self.text_type}, {repr(self.url)})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.REGULAR:
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
            return LeafNode("img", None, {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.REGULAR:
            new_nodes.append(node)
            continue

        node_text_split = node.text.split(delimiter)
        if (len(node_text_split) % 2) == 0:
            raise Exception(
                f"No closing delimiter {delimiter} found when parsing {node}"
            )
        for i, text in enumerate(node_text_split):
            if (i % 2) == 0:
                new_nodes.append(TextNode(text, TextType.REGULAR))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes
