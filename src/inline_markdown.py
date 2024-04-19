from textnode import TextNode, TextType

import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_nodes.extend(split_text(node.text, delimiter, text_type))
        else:
            new_nodes.append(node)
    
    return new_nodes

def split_text(text, delimiter, text_type):
    sections = text.split(delimiter)
    new_nodes = []
    if len(sections) % 2 == 0:
        raise Exception("Need a closing and an opening delimiter")
    for i in range(0, len(sections)):
        if len(sections[i]) == 0:
            continue
        if not i % 2 == 0:
            new_nodes.append(TextNode(sections[i], text_type))
        else:
            new_nodes.append(TextNode(sections[i], TextType.TEXT))
    return new_nodes


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
