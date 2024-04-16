from enum import Enum

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    UNORDERED_LIST = 3
    ORDERED_LIST = 4
    CODE_BLOCK = 5
    QUOTE_BLOCK = 6

def markdown_to_blocks(markdown):
    filtered_blocks = filter(lambda block : len(block) > 0, markdown.split("\n\n"))
    return list(map(lambda block : block.strip(), filtered_blocks))

def get_block_type(block):
    if block.startswith("* ") or block.startswith("- "):
        return BlockType.UNORDERED_LIST if valid_unordered_list(block) else BlockType.PARAGRAPH
    if block.startswith("#"):
        return BlockType.HEADING if valid_heading(block) else BlockType.PARAGRAPH
    if block[0].isdigit() and block[1:].startswith(". "):
        return BlockType.ORDERED_LIST if valid_ordered_list(block) else BlockType.PARAGRAPH
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE_BLOCK 
    if block.startswith(">"):
        return BlockType.QUOTE_BLOCK if valid_quote(block) else BlockType.PARAGRAPH
    return BlockType.PARAGRAPH

def valid_unordered_list(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith("* ") and not line.startswith("- "):
            return False 

    return True

def valid_ordered_list(block):
    lines = block.split("\n")
    for i in range(0, len(lines)):
        if not (lines[i].startswith(f"{i + 1}. ")):
            return False
    return True


def valid_heading(block):
    hash_counter = 0
    first_space = block.find(" ")
    for i in range(0, first_space):
        if block[i] != "#":
            return False
        hash_counter += 1
    return True if hash_counter <= 6 else False

def valid_quote(block):
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            return False
    return True

