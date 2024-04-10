class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        prop_string = ""
        for prop in self.props:
            prop_string += f" {prop}=\"{self.props[prop]}\""
        
        return prop_string


    def __repr__(self):
        result = f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
        return result
    


class LeafNode(HtmlNode):
    def __init__(self, value, tag=None, props=None):
        if value == None:
            raise ValueError("Value must be supplied")
        if props != None and tag == None:
            raise Exception("Cannot have props without a tag")
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag == None:
            return self.value
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"

        return opening_tag + self.value + closing_tag
    
    def __repr__(self):
        return f"LeafNode({self.value}, {self.tag}, {self.props})"
    

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        if tag == None:
            raise ValueError("Must provide a tag")
        if children == None:
            raise ValueError("ParentNode must have children")
        
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        opening_tag = f"<{self.tag}{self.props_to_html()}>"
        closing_tag = f"</{self.tag}>"
        body = ""

        for child in self.children:
            body += child.to_html()

        return opening_tag + body + closing_tag
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"



        