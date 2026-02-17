class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join(f'{key}="{value}"' for (key, value) in self.props.items())

    def __repr__(self):
        return f"HTMLNode({repr(self.tag)}, {repr(self.value)}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError(f"Leaf node {self} has no value")

        if self.tag is None:
            return self.value
        else:
            props = self.props_to_html()
            props = (
                " " + props if props != "" else ""
            )  # add a space to beginning if not empty
            return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"TextNode({repr(self.tag)}, {repr(self.value)}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError(f"Text Node {self} has no tag")
        if self.children is None:
            raise ValueError(f"Text Node {self} has no children")

        children_html = "".join(child.to_html() for child in self.children)
        props = self.props_to_html()
        props = (
            " " + props if props != "" else ""
        )  # add a space to beginning if not empty
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"
