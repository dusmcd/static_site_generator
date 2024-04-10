from htmlnode import LeafNode
from enum import Enum

class TextType(Enum):
    TEXT = 1
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
        return (self.text == other.text and 
                self.text_type == other.text_type and 
                self.url == other.url)
    
    def text_node_to_html_node(self):
        type = self.text_type

        if type == TextType.TEXT:
            return LeafNode(self.text)
        elif type == TextType.BOLD:
            return LeafNode(self.text, "b")
        elif type == TextType.ITALIC:
            return LeafNode(self.text, "i")
        elif type == TextType.CODE:
            return LeafNode(self.text, "code")
        elif type == TextType.LINK:
            return LeafNode(self.text, "a", {"href": self.url})
        elif type == TextType.IMAGE:
            return LeafNode(self.text, "img", {"src": self.url, "alt": self.text})
        
        raise Exception("Given type not recognized")
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    