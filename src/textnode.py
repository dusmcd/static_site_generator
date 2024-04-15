from htmlnode import LeafNode
from enum import Enum
from extract import extract_markdown_images, extract_markdown_links

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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_text(node.text, delimiter, text_type))
        else:
            new_nodes.append(node)
    
    return new_nodes

def split_text(text, delimiter, text_type):
    words = text.split()
    indices_with_delimiter = get_delimiter_info(words, delimiter)
    new_nodes = []
    sections = filter(lambda section : len(section) > 0, text.split(delimiter))
    word_count = -1
    j = 0
    for section in sections:
        word_count += len(section.split())
        if j >= len(indices_with_delimiter):
            new_nodes.append(TextNode(section, TextType.TEXT))
        elif word_count < indices_with_delimiter[j]:
            new_nodes.append(TextNode(section, TextType.TEXT))
        elif word_count >= indices_with_delimiter[j]:
            new_nodes.append(TextNode(section, text_type))
            j += 1
        

    return new_nodes

def get_delimiter_info(words, delimiter):
    indices_with_delimiter = []
    delimiter_check = 0
    for i in range(0, len(words)):
        if delimiter in words[i][0:2] and delimiter in words[i][len(words[i]) - 2:]:
            indices_with_delimiter.append(i)
            delimiter_check = 0
        elif delimiter in words[i][0:2]:
            indices_with_delimiter.append(i)
            delimiter_check += 1
        elif delimiter in words[i][len(words[i]) - 2:]:
            delimiter_check -= 1

    
    if delimiter_check != 0:
        raise Exception("Need a closing and an opening delimiter")
    return indices_with_delimiter

def split_images_links(extracter, parser, marker, text_type):
    def splitter(old_nodes):
        new_nodes = []
        for node in old_nodes:
            assets = extracter(node.text)
            if len(assets) == 0:
                new_nodes.append(node)
            else:
                new_nodes.extend(parser(node.text, assets, marker, text_type))
        return new_nodes
    return splitter


def parser(text, assets, marker, text_type):
    new_nodes = []
    current_text = text
    for asset in assets:
        sections = current_text.split(f"{marker}[{asset[0]}]({asset[1]})")
        if len(sections[0]) == 0:
            new_nodes.append(TextNode(asset[0], text_type, asset[1]))
        else:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(asset[0], text_type, asset[1]))
        current_text = sections[1]
    if len(current_text) > 0:
        new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

split_nodes_images = split_images_links(extract_markdown_images, parser, "!", TextType.IMAGE)
split_nodes_links = split_images_links(extract_markdown_links, parser, "", TextType.LINK)

def text_to_text_nodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes
