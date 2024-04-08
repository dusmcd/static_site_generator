class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

        if tag == None and value == None:
            raise Exception("No tag requires a value property")
        if value == None and children == None:
            raise Exception("Must have at least either chidren or a value")
        if tag == None and props != None:
            raise Exception("Cannot have attributes without a tag")

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
        opening_tag = f"<{self.tag}" if self.tag != None else ""
        closing_tag = f"</{self.tag}>" if self.tag != None else ""

        opening_tag += self.props_to_html() + ">"

        return opening_tag + self.value + closing_tag
    
html_node2 = HtmlNode("a", "link", None, {"href": "https://www.something.com"})
html_node2.props_to_html()

