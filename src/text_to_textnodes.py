import re

from textnode import TextNode, TextType


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


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.REGULAR:
            new_nodes.append(node)
            continue

        text_array = re.split(r"!\[.*?\]\(.*?\)", node.text)
        images_array = extract_markdown_images(node.text)

        text_nodes = [TextNode(text, TextType.REGULAR) for text in text_array]
        image_nodes = [
            TextNode(image[0], TextType.IMAGE, image[1]) for image in images_array
        ]

        nodes = []
        for i in range(len(text_nodes)):
            if text_nodes[i].text != "":  # discard empty nodes
                nodes.append(text_nodes[i])

            if i < len(image_nodes):
                nodes.append(image_nodes[i])

        new_nodes.extend(nodes)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.REGULAR:
            new_nodes.append(node)
            continue

        text_array = re.split(r"\[.*?\]\(.*?\)", node.text)
        link_array = extract_markdown_links(node.text)

        text_nodes = [TextNode(text, TextType.REGULAR) for text in text_array]
        link_nodes = [TextNode(link[0], TextType.LINK, link[1]) for link in link_array]

        nodes = []
        for i in range(len(text_nodes)):
            if text_nodes[i].text != "":  # discard empty nodes
                nodes.append(text_nodes[i])

            if i < len(link_nodes):
                nodes.append(link_nodes[i])

        new_nodes.extend(nodes)

    return new_nodes


def text_to_textnodes(text):
    orig_node = TextNode(text, TextType.REGULAR)
    after_bold = split_nodes_delimiter([orig_node], "**", TextType.BOLD)
    after_italic = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
    after_code = split_nodes_delimiter(after_italic, "`", TextType.CODE)
    after_image = split_nodes_image(after_code)
    after_link = split_nodes_link(after_image)
    return after_link
