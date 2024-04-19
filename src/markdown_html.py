from inline_markdown import text_to_text_nodes
from htmlnode import ParentNode
from block_markdown import markdown_to_blocks, get_block_type, BlockType

def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    blocks_and_types = map(lambda block : {"type": get_block_type(block), "text": block}, blocks)
    html_parent_nodes = []
    for block in blocks_and_types:
        if block["type"] == BlockType.PARAGRAPH:
            html_parent_nodes.append(convert_paragraphs(block))
        elif block["type"] == BlockType.HEADING:
            html_parent_nodes.append(convert_headings(block))
        elif block["type"] == BlockType.UNORDERED_LIST:
            html_parent_nodes.append(convert_unordered_lists(block))
        elif block["type"] == BlockType.ORDERED_LIST:
            html_parent_nodes.append(convert_ordered_lists(block))
        elif block["type"] == BlockType.QUOTE_BLOCK:
            html_parent_nodes.append(convert_quote_blocks(block))
        elif block["type"] == BlockType.CODE_BLOCK:
            html_parent_nodes.append(convert_code_blocks(block))
    
    html_body = ""
    for node in html_parent_nodes:
        html_body += node.to_html()
    return f"<div>{html_body}</div>"


def convert_paragraphs(block):
    text_nodes = text_to_text_nodes(block["text"])
    children = []
    for node in text_nodes:
        children.append(node.text_node_to_html_node())
    return ParentNode("p", children)

def convert_headings(block):
    text_nodes = text_to_text_nodes(block["text"])
    children = []
    header_type = text_nodes[0].text.find(" ")
    first_node_text = text_nodes[0].text.lstrip("# ")
    text_nodes[0].text = first_node_text
    for node in text_nodes:
        children.append(node.text_node_to_html_node())
    return ParentNode(f"h{header_type}", children)

def convert_unordered_lists(block):
    lines = block["text"].split("\n")
    children = []
    for line in lines:
        line = line.lstrip("* ") if line.startswith("*") else line.lstrip("- ")
        list_items_html_nodes = map(lambda node : node.text_node_to_html_node(), text_to_text_nodes(line))
        children.append(ParentNode("li", list_items_html_nodes))
    return ParentNode("ul", children)

def convert_ordered_lists(block):
    lines = block["text"].split("\n")
    children = []
    for line in lines:
        first_space = line.find(" ")
        line = line[first_space + 1:]
        list_items_html_nodes = map(lambda node : node.text_node_to_html_node(), text_to_text_nodes(line))
        children.append(ParentNode("li", list_items_html_nodes))
    return ParentNode("ol", children)

def convert_quote_blocks(block):
    children = []
    clean_lines = map(lambda line : line.lstrip(">"), block["text"].split("\n"))
    text_nodes = text_to_text_nodes("<br>".join(clean_lines))
    for node in text_nodes:
        children.append(node.text_node_to_html_node())
    return ParentNode("blockquote", children)

def convert_code_blocks(block):
    children = []
    text_nodes = text_to_text_nodes(block["text"].strip("```").replace("\n", "<br>"))
    for node in text_nodes:
        children.append(node.text_node_to_html_node())
    return ParentNode("pre", [ParentNode("code", children)])