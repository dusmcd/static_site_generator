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
        children_html = ""
        opening_tag += self.props_to_html() + ">"
        if self.children != None:
            for child in self.children:
                children_html += child.__repr__()

        return f"{opening_tag}{children_html}{self.value if self.value != None else ""}{closing_tag}"
    


