import unittest

from block import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        text = "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line"
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

    def test_heading(self):
        text = "## This is a heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_code(self):
        text = '```\nprint("Hello World!")\n```'
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_quote(self):
        text = ">This is a quote\n>line 2"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_unordered_list(self):
        text = "- This is a list\n- with items"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        text = "1. This is an ordered list\n2. with items"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
