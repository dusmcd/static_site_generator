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

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
        else:
            new_nodes = split_text_and_images(node.text, images)
    return new_nodes

def split_text_and_images(text, images):
    updated_text = text
    for image in images:
        updated_text = updated_text.replace(f"![{image[0]}]({image[1]})", "![IMAGE]")
    words = updated_text.split()
    new_nodes = []
    text_block = ""
    j = 0
    for i in range(0, len(words)):
        if words[i] == "![IMAGE]":
            new_nodes.append(TextNode(text_block + " ", TextType.TEXT)) if len(text_block) > 0 else None
            text_block = ""
            new_nodes.append(TextNode(images[j][0], TextType.IMAGE, images[j][1]))
            j += 1
        elif i == len(words) - 1:
            text_block += " " + words[i]
            new_nodes.append(TextNode(text_block, TextType.TEXT))
        else:
            text_block += words[i] if i == 0 else " " + words[i] 
    return new_nodes

