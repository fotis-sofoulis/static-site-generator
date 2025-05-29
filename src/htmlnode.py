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
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}=\"{self.props[prop]}\"'
        return props_html

    def __repr__(self):
        return f"{self.__class__.__name__}(tag={self.tag},"\
            f"value={self.value}, children={self.children},)"\
            f"props={self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props=props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value is None:
            raise ValueError("no given value")
        elif not self.tag:
            return f'{self.value}'
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props=props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if not self.tag:
            raise ValueError("no given tag")
        if self.children is None:
            raise ValueError("no children given")
        if len(self.children) == 0:
            raise ValueError("empty children list")

        final_html = f'<{self.tag}>'
        for child in self.children:
            final_html += child.to_html()
        final_html += f'</{self.tag}>'

        return final_html
