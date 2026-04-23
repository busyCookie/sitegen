class HTMLNode:

    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return ( (self.tag == other.tag)
            and (self.value == other.value)
            and (self.children == other.children)
            and (self.props == self.props) )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props}, {self.children})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_props = ""

        if self.props:
            for prop in self.props:
                html_props = f"{html_props} {prop}=\"{self.props[prop]}\""

        return html_props

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if not self.value:
            return ValueError("Tag is empty")

        if not self.tag:
            return f"{self.value}"

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            return ValueError("Tag is not defined")

        html_children = ""

        for child in self.children:
            html_children += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{html_children}</{self.tag}>"
