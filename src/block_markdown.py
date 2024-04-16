
def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    block_text = ""
    blocks = []
    for i in range(0, len(lines)):
        block_text += lines[i] 
        if len(lines[i]) == 0:
            blocks.append(block_text.strip())
            block_text = ""
    if len(block_text) > 0:
        blocks.append(block_text.strip())

    return blocks


