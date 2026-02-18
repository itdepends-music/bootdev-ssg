import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_2(self):
        node = TextNode("This is a text node", TextType.IMAGE, "")
        node2 = TextNode("This is a text node", TextType.IMAGE, "")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.IMAGE, "Link")
        node2 = TextNode("This is a text node", TextType.LINK, "Link")
        self.assertNotEqual(node, node2)


class TestTextNodeToHTML_NODE(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.REGULAR)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("cat picture", TextType.IMAGE, "/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src": "/cat.png", "alt": "cat picture"})


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle", TextType.REGULAR
        )
        split = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(split), 3)
        self.assertEqual(split[0].text, "This is text with a ")
        self.assertEqual(split[0].text_type, TextType.REGULAR)
        self.assertEqual(split[1].text, "bolded phrase")
        self.assertEqual(split[1].text_type, TextType.BOLD)
        self.assertEqual(split[2].text, " in the middle")
        self.assertEqual(split[2].text_type, TextType.REGULAR)


if __name__ == "__main__":
    unittest.main()
